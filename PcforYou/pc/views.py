from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from functools import wraps
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .utils import call_gemini_api
import json
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile


# Create your views here.
def index(request):
    
    prebuilt_pcs = PrebuiltPC.objects.all().order_by('-created_at')[:4] 

    return render(request, 'index.html',{'prebuilts':prebuilt_pcs})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            if user.is_staff:
                login(request,user)
                request.session['is_admin_logged_in'] = True
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You are not authorized to access admin panel.')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'admin/admin_login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


#Custom Decorator for Admin Panel Access
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            # messages.error(request, "You must login as admin to access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    product_count = Product.objects.count()
    # prebuit_count = PrebuiltPC.objects.count()
    category_count = Category.objects.count()
    recent_orders = Order.objects.order_by("-created_at")[:5]

    return render(request,'admin/admin_dashboard.html',{'product_count':product_count,'category_count':category_count,"recent_orders":recent_orders})

@admin_required
def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save()  # category now bound correctly
            cat_slug = product.category.slug.lower()

            form_map = {
                "processor": CPUDetailsForm,
                "graphics-card": GPUDetailsForm,
                "gpu": GPUDetailsForm,
                "ram": RAMDetailsForm,
                "storage": StorageDetailsForm,
                "monitor": MonitorDetailsForm,
                "cooling": CoolingDetailsForm,
                "motherboard": MotherboardDetailsForm,
                "power-supply": PowerSupplyDetailsForm,
                "cabinet": CabinetDetailsForm,
                "accessory": AccessoryDetailsForm,
                "accessories": AccessoryDetailsForm,
            }

            if cat_slug in form_map:
                detail_form = form_map[cat_slug](request.POST)
                if detail_form.is_valid():
                    detail = detail_form.save(commit=False)
                    detail.product = product
                    detail.save()
                else:
                    print(detail_form.errors)

            # messages.success(request, "✅ Product added successfully!")
            return redirect('view_products')
        else:
            print(product_form.errors)
            messages.error(request, "⚠️ Please fix the errors below.")

    else:
        product_form = ProductForm()

    return render(request, "admin/add_products.html", {
        "product_form": product_form,
        "categories": categories,
    })

# ----------for users ----------
def prebuilt_list(request):
    prebuilts = PrebuiltPC.objects.all().order_by('-created_at')
    return render(request, 'users/prebuilt_list.html', {'prebuilts': prebuilts})

def prebuilt_detail(request, id):
    pc = get_object_or_404(PrebuiltPC, id=id)
    return render(request, 'users/prebuilt_detail.html', {'pc': pc})
# ----------------------------------
    
@admin_required
def viewproducts(request):

    categories = Category.objects.all().order_by('name')
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id).select_related('category').order_by('name')
    else:
        products = Product.objects.select_related('category').all().order_by('category__name', 'name')

    return render(request,'admin/view_products.html',
                {   'products':products , 
                    'categories': categories, 
                    'selected_category': int(category_id) if category_id else None,
                })

@admin_required
def prebuiltview(request):

    prebuilt_pcs = PrebuiltPC.objects.all().order_by('-created_at')  
    context = {
        'prebuilt_pcs': prebuilt_pcs
    }
    return render(request,'admin/prebuilt_pc.html',context)

@admin_required
def prebuilt_pc_detail(request, slug):
    # Retrieve the PC based on the slug, or return 404 if not found
    pc = get_object_or_404(PrebuiltPC, slug=slug)
    context = {
        'pc': pc
    }
    return render(request, 'admin/pc_details.html',context)

@admin_required
def add_prebuilt(request):

    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        slug = request.POST['slug']
        image = request.FILES.get('image')
        description = request.POST['description']
        processor = request.POST['processor']
        graphics_card = request.POST['graphics_card']
        motherboard = request.POST['motherboard']
        ram = request.POST['ram']
        storage = request.POST['storage']
        power_supply = request.POST['power_supply']
        cooling = request.POST['cooling']
        cabinet = request.POST['cabinet']
        monitor = request.POST['monitor']
        accessories = request.POST['accessories']

        data = PrebuiltPC.objects.create(name=name,slug=slug,image=image,price=price,description=description,processor=processor,
                                         motherboard=motherboard,graphics_card=graphics_card,ram=ram,storage=storage,power_supply=power_supply,
                                         cooling=cooling,cabinet=cabinet,monitor=monitor,accessories=accessories)
        data.save()
        # messages.success(request,'prebuilt pc added')
        return redirect('prebuilt_view')
    return render(request,'admin/add_prebuilt.html')

def cabinets(request):

    category = get_object_or_404(Category,name='Cabinet')
    products = Product.objects.filter(category=category,is_available = True)

     # ------- PRICE (single slider named "price") -------
    max_price = request.GET.get("price")
    try:
        if max_price is not None and str(max_price).strip() != "":
            max_price_int = int(max_price)
            products = products.filter(price__lte=max_price_int)
        else:
            max_price_int = None
    except (ValueError, TypeError):
        # If someone passes a bad value, ignore it
        max_price_int = None

    # ------- FORM FACTOR -------
    form_factors = request.GET.getlist("form_factor")  # multiple values possible
    if form_factors:
        from django.db.models import Q
        q = Q()

        for ff in form_factors:
            words = ff.split()  # split "Mini Tower" → ["Mini", "Tower"]

            sub_q = Q()
            for w in words:
                sub_q &= Q(cabinet_details__form_factor__icontains=w)

            q |= sub_q

        products = products.filter(q)
    return render(request, "users/cabinets.html", {"cabinet":products,"selected_form_factors": form_factors,
        "max_price": max_price,})

def cooling(request):
    category = get_object_or_404(Category, name="Cooling")
    products = Product.objects.filter(category=category, is_available=True)

    # Price filter
    max_price = request.GET.get("price")
    if max_price:
        products = products.filter(price__lte=max_price)

    # Cooling type filter
    selected_types = request.GET.getlist("cooling_type")  # <-- IMPORTANT

    if selected_types:
        products = products.filter(cooling_details__cooling_type__in=selected_types)

    return render(request, "users/cooling.html", {
        "cooling": products,
        "selected_types": selected_types,
        "max_price": max_price,
    })

def ram(request):

    category = get_object_or_404(Category,name="RAM")
    products = Product.objects.filter(category=category,is_available = True)

    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte=max_price)

     # --- RAM TYPE FILTER (DDR4 / DDR5) ---
    selected_types = request.GET.getlist("ram_type")
    if selected_types:
        products = products.filter(ram_details__ddr_type__in=selected_types)

    # --- RAM SIZE FILTER (8, 16, 32...) ---
    selected_sizes = request.GET.getlist("size")
    if selected_sizes:
        products = products.filter(ram_details__capacity_gb__in=selected_sizes)

    ram_sizes = [8, 16, 32, 64, 128]

    return render(request, "users/ram.html", {
        "rams": products,
        "selected_types": selected_types,
        "selected_sizes": selected_sizes,
        "ram_sizes": ram_sizes,
    })

def gpu(request):
    category = get_object_or_404(Category, name="Graphics Card")
    products = Product.objects.filter(category=category, is_available=True)

    # --- PRICE FILTER ---
    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte=max_price)

    # --- VRAM FILTER (4, 6, 8, 12, 16 GB) ---
    selected_vram = request.GET.getlist("vram")
    if selected_vram:
        products = products.filter(gpu_details__vram_gb__in=selected_vram)

    # --- BRAND FILTER ---
    selected_brands = request.GET.getlist("brand")
    if selected_brands:
        brand_query = Q()
        for brand in selected_brands:
            brand_query |= Q(name__icontains=brand)

        products = products.filter(brand_query)  # simple contains, or create a brand field

    # Options for filters
    vram_options = [ 8, 12, 16, 24, 32, 64]
    brand_options = ["NVIDIA", "AMD"]  # or populate dynamically from products

    return render(request, "users/graphics_card.html", {
        "gpus": products,
        "selected_vram": selected_vram,
        "vram_options": vram_options,
        "selected_brands": selected_brands,
        "brand_options": brand_options,
    })


def processors(request):
    category = get_object_or_404(Category, name="Processor")
    products = Product.objects.filter(category=category, is_available=True)

    # --- PRICE FILTER ---
    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte=max_price)


    # --- BRAND FILTER ---
    # selected_brands = request.GET.getlist("brand")
    # if selected_brands:
    selected_brands = request.GET.getlist("brand")
    if selected_brands:
        brand_query = Q()
        for brand in selected_brands:
            brand_query |= Q(name__icontains=brand)

        products = products.filter(brand_query)  # simple contains, or create a brand field

    # Options for filters
    brand_options = ["Intel", "AMD"]

    return render(request, "users/processors.html", {
        "processors": products,
        "selected_brands": selected_brands,
        "brand_options": brand_options,
    })

def monitors(request):
    category = get_object_or_404(Category,name="Monitor")
    products = Product.objects.filter(category=category,is_available = True)

    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte=max_price)

    selected_size = request.GET.getlist('size')
    if selected_size:
        products = products.filter(monitor_details__size_inch__in=selected_size)

    size_options = [24 , 27 , 32 , 34 ]

    return render(request,'users/monitors.html',{
        "monitors" : products,
        "selected_size" : selected_size,
        "size_options" : size_options
    })

def motherboards(request):
    category = get_object_or_404(Category,name="Motherboard")
    products = Product.objects.filter(category=category,is_available = True)

    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte = max_price)

    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        brand_query = Q()
        for brand in selected_brands:
            brand_query |= Q(name__icontains=brand)

        products = products.filter(brand_query)  # simple contains, or create a brand field

    # Options for filters
    brand_options = ["ASUS", "MSI" , "GIGABYTE"]

    return render(request, "users/motherboard.html", {
        "motherboards": products,
        "selected_brands": selected_brands,
        "brand_options": brand_options,
    })

def powersupply(request):
    category = get_object_or_404(Category,name="Power Supply")
    products = Product.objects.filter(category=category,is_available = True)

    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte = max_price)

    return render(request,'users/powersupply.html',{
        "powersupply" : products
    })
# Product - detail - page ----------------------------

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    details = None

    # Dynamically detect details based on category
    if hasattr(product, "ram_details"):
        details = product.ram_details
    elif hasattr(product, "cabinet_details"):
        details = product.cabinet_details
    elif hasattr(product, "cooling_details"):
        details = product.cooling_details
    elif hasattr(product,"gpu_details"):
        details = product.gpu_details
    elif hasattr(product,"cpu_details"):
        details = product.cpu_details
    elif hasattr(product,'monitor_details'):
        details = product.monitor_details
    elif hasattr(product,"motherboard_details"):
        details = product.motherboard_details
    elif hasattr(product,'powersupply_details'):
        details = product.powersupply_details
    # Add more if needed

    return render(request, "users/product_detail.html", {
        "product": product,
        "details": details,
    })

# -----------------------------------------------------------------

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Prevent duplicates
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    # if created:
    #     messages.success(request, f"{product.name} added to your wishlist.")
    # else:
    #     messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect(request.META.get("HTTP_REFERER", "wishlist"))

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product", "product__category")
    total_price = sum(item.product.price for item in wishlist_items)

    return render(request, "users/wishlist.html", {
        "wishlist_items": wishlist_items,
        'total_price':total_price
    })


@login_required
def remove_from_wishlist(request, product_id):
    item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    item.delete()
    return redirect("wishlist")

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related("product", "product__category")

    subtotal = sum(item.total_price for item in cart_items)
    shipping = Decimal('30') if subtotal > 0 else Decimal(0.00)
    estimated_tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))   # 8% example
    total = subtotal + shipping + estimated_tax

    return render(request, "users/cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "estimated_tax": estimated_tax,
        "total": total,
    })

@login_required
def update_cart_quantity(request, cart_id, action):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect("cart")

@login_required
def remove_from_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id, user=request.user)
    item.delete()
    return redirect("cart")


@login_required
def checkout_cart(request, product_id=None):
    # BUY NOW MODE
    if product_id:
        product = Product.objects.get(id=product_id)

        # Create a fake cart-like object to reuse code
        class TempItem:
            def __init__(self, product):
                self.product = product
                self.quantity = 1
                self.total_price = product.price

        cart_items = [TempItem(product)]

    else:
        # NORMAL CART MODE
        cart_items = list(Cart.objects.filter(user=request.user))
        if not cart_items:
            return redirect('cart')

    # --- PRICE CALCULATIONS ---
    subtotal = sum(item.total_price for item in cart_items)
    shipping = Decimal('30') if subtotal > 0 else Decimal('0.00')
    estimated_tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))
    total = subtotal + shipping + estimated_tax

    # --- HANDLE ORDER SUBMISSION ---
    if request.method == "POST":
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            address=address
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart only if it was a CART checkout
        if not product_id:
            Cart.objects.filter(user=request.user).delete()

        return redirect('order_detail', order_id=order.id)

    return render(request, 'users/checkout_cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'estimated_tax': estimated_tax,
        'total': total
    })

@login_required
def buy_prebuilt(request, pc_id):
    prebuilt = PrebuiltPC.objects.get(id=pc_id)

    # Fake cart-like item
    class TempItem:
        def __init__(self, pc):
            self.product = pc  # reusing product variable name in template
            self.quantity = 1
            self.total_price = pc.price

    cart_items = [TempItem(prebuilt)]

    # Price calculation
    subtotal = prebuilt.price
    shipping = Decimal('30') if subtotal > 0 else Decimal('0.00')
    estimated_tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))
    total = subtotal + shipping + estimated_tax

    # When form is submitted
    if request.method == "POST":
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            address=address
        )

        # Store as PrebuiltPC order
        OrderItem.objects.create(
            order=order,
            prebuilt_pc=prebuilt,
            quantity=1,
            price=prebuilt.price
        )

        return redirect('order_detail', order_id=order.id)

    return render(request, 'users/checkout_cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'estimated_tax': estimated_tax,
        'total': total
    })

@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "users/orders_list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST" and 'cancel_order' in request.POST:
        if order.status in ["PENDING", "CONFIRMED"]:
            order.status = "CANCELLED"
            order.save()
    return render(request, 'users/order_detail.html', {'order': order})


@admin_required
def admin_order_manage(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/order_manage.html', {'orders': orders})

@require_POST
@admin_required
def update_order_status(request):
    order_id = request.POST.get('order_id')
    new_status = request.POST.get('new_status')

    order = get_object_or_404(Order, pk=order_id)
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        return JsonResponse({'success': True, 'new_status': order.status})
    return JsonResponse({'success': False, 'error': 'Invalid status'})

# -------------------------pc builder compactability-----------------------------------

def pc_builder(request):
    context = {
        "parts": ["CPU", "Motherboard", "RAM", "GPU", "Storage", "Cooling", "PSU", "Case"],
        "cpus": Product.objects.filter(category__name="Processor"),
        "gpus": Product.objects.filter(category__name="Graphics Card"),
        "motherboards": Product.objects.filter(category__name="Motherboard"),
        "rams": Product.objects.filter(category__name="RAM"),
        "storages": Product.objects.filter(category__name="Storage"),
        "psus": Product.objects.filter(category__name="Power Supply"),
        "cases": Product.objects.filter(category__name="Cabinet"),
        "coolings": Product.objects.filter(category__name="Cooling"),
    }
    return render(request, "users/pc_builder.html", context)

@csrf_exempt
def gemini_compat_check(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)
            
        prompt = data.get("prompt")
        
        if not prompt:
            return JsonResponse({"error": "No prompt provided"}, status=400)

        # 1. Call the updated Gemini API utility function
        result_text = call_gemini_api(prompt)

        # 2. Check for the error prefix from utils.py
        if result_text.startswith("ERROR:"):
            # Return a 500 status if the utility function signalled an error
            return JsonResponse({"error": result_text}, status=500)
            
        # 3. Success
        return JsonResponse({"response": result_text})

    return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=400)

#-------------------pdf report ---------------------------------------------------
def generate_report_pdf(request):
    if request.method == "POST":
        data = json.loads(request.body)

        selected_parts = data.get("selected_parts", {})
        ai_report = data.get("ai_report", "")

        # Render HTML template → string
        html_string = render_to_string("users/report.html", {
            "selected_parts": selected_parts,
            "ai_report": ai_report
        })

        # Create PDF file in memory
        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=PC_Compatibility_Report.pdf"
        return response