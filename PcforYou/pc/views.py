from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from functools import wraps
from .models import *
from .forms import *

# Create your views here.
def index(request):
    
    return render(request, 'index.html')

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
            messages.error(request, "You must login as admin to access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    product_count = Product.objects.count()
    prebuit_count = PrebuiltPC.objects.count()
    return render(request,'admin/admin_dashboard.html')

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

            messages.success(request, "✅ Product added successfully!")
            return redirect('add_products')
        else:
            print(product_form.errors)
            messages.error(request, "⚠️ Please fix the errors below.")

    else:
        product_form = ProductForm()

    return render(request, "admin/add_products.html", {
        "product_form": product_form,
        "categories": categories,
    })


    
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