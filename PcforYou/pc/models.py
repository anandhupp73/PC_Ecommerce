from django.db import models
import os,uuid
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    allow_multiple = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
        
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

def product_image_upload_path(instance, filename):
    """
    Store images inside media/products/<category-slug>/<filename>.
    Example: media/products/processor/intel-i9.jpg
    """
    category_slug = slugify(instance.category.name)
    base, ext = os.path.splitext(filename)
    unique_name = f"{slugify(base)}-{uuid.uuid4().hex[:6]}{ext}"
    return f"products/{category_slug}/{unique_name}"

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=product_image_upload_path,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock_quantity = models.PositiveBigIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.category.name} : {self.name}"
    
    def get_detail(self):
        """Return the related detail object based on category"""
        detail_map = {
            'Processor' : 'cpu_details',
            'Graphics Card': 'gpu_details',
            'RAM': 'ram_details',
            'Storage': 'storage_details',
            'Monitor': 'monitor_details',
            'Cooling': 'cooling_details',
            'Motherboard': 'motherboard_details',
            'Power Supply': 'powersupply_details',
            'Cabinet': 'cabinet_details',
            'Accessories': 'accessory_details',
        }
        related_name = detail_map.get(self.category.name)
        if related_name:
            return getattr(self,related_name,None)
        return None
    
class CPUDetails(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE, related_name='cpu_details')
    core_count = models.PositiveIntegerField()
    thread_count = models.PositiveIntegerField()
    base_clock_ghz = models.DecimalField(max_digits=4,decimal_places=2)
    socket_type = models.CharField(max_length=50)

class GPUDetails(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE, related_name='gpu_details')
    vram_gb = models.PositiveIntegerField()
    chipset = models.CharField(max_length=100)
    interface = models.CharField(max_length=50,default='PCIe 4.0')

class RAMDetails(models.Model):
    # product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='ram_details')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='ram_details')
    capacity_gb = models.PositiveIntegerField()
    speed_mhz = models.PositiveIntegerField()
    ddr_type = models.CharField(max_length=10) #DDR4,DDR5
    module_count = models.PositiveIntegerField(default=1)

class StorageDetails(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE, related_name='storage_details')
    capacity_gb = models.PositiveIntegerField()
    storage_type = models.CharField(max_length=10, choices=[
        ('HDD','HDD'),
        ('SSD','SSD'),
        ('NVMe','NVMe SSD')
    ])
    form_factor = models.CharField(max_length=20)

class MonitorDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='monitor_details')
    size_inch = models.DecimalField(max_digits=4, decimal_places=1)
    resolution = models.CharField(max_length=50)
    refresh_rate_hz = models.PositiveIntegerField()
    panel_type = models.CharField(max_length=50, blank=True, null=True)

class CoolingDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='cooling_details')
    cooling_type = models.CharField(max_length=50)  # Air, Liquid
    fan_count = models.PositiveIntegerField(blank=True, null=True)

class MotherboardDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='motherboard_details')
    chipset = models.CharField(max_length=50)
    socket_type = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=20)

class PowerSupplyDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='powersupply_details')
    wattage = models.PositiveIntegerField()
    efficiency_rating = models.CharField(max_length=30, blank=True, null=True)
    modular = models.CharField(max_length=20,blank=True,null=True)

class CabinetDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='cabinet_details')
    form_factor = models.CharField(max_length=50)  # e.g., ATX, Micro-ATX
    color = models.CharField(max_length=50, blank=True, null=True)

class AccessoryDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='accessory_details')
    accessory_type = models.CharField(max_length=20, choices=[
        ('Mouse', 'Mouse'),
        ('Keyboard', 'Keyboard'),
        ('Headset', 'Headset'),
        ('Monitor', 'Monitor'),
        ('Other', 'Other'),
    ])
    connection = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

def prebuilt_image_upload_path(instance, filename):
    base, ext = os.path.splitext(filename)
    unique_name = f"{slugify(base)}-{uuid.uuid4().hex[:6]}{ext}"
    return f"prebuilt_pcs/{unique_name}"

class PrebuiltPC(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=prebuilt_image_upload_path, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # System Specifications
    processor = models.CharField(max_length=255)
    motherboard = models.CharField(max_length=255)
    graphics_card = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)
    power_supply = models.CharField(max_length=255)
    cooling = models.CharField(max_length=255, blank=True, null=True)
    cabinet = models.CharField(max_length=255, blank=True, null=True)
    monitor = models.CharField(max_length=255, blank=True, null=True)
    accessories = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Prebuilt PC"
        verbose_name_plural = "Prebuilt PCs"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="wishlist_items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username}->{self.product.name}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="in_carts")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} -> {self.product.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("SHIPPED", "Shipped"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)

    # Allow either Product OR PrebuiltPC
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    prebuilt_pc = models.ForeignKey(PrebuiltPC, null=True, blank=True, on_delete=models.SET_NULL)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        if self.product:
            return f"{self.product.name} x {self.quantity}"
        elif self.prebuilt_pc:
            return f"{self.prebuilt_pc.name} (Prebuilt) x {self.quantity}"
        return "Unknown Item"
    

class Profile(models.Model):
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    display_name = models.CharField(max_length=100, blank=True)
    user_phone = models.CharField(max_length=15, blank=True)
    user_address = models.TextField(blank=True)
    user_city = models.CharField(max_length=100, blank=True)
    user_state = models.CharField(max_length=100, blank=True)
    user_pincode = models.CharField(max_length=10, blank=True)
    user_image = models.ImageField(upload_to="profiles/", default="profiles/default.png",blank=True,null=True)

    def __str__(self):
        return self.profile_user.username