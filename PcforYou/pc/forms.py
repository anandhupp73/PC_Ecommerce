from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'description', 'price', 'stock_quantity', 'is_available']

class CPUDetailsForm(forms.ModelForm):
    class Meta:
        model = CPUDetails
        fields = ['core_count', 'thread_count', 'base_clock_ghz', 'socket_type']

class GPUDetailsForm(forms.ModelForm):
    class Meta:
        model = GPUDetails
        fields = ['vram_gb', 'chipset', 'interface']

class RAMDetailsForm(forms.ModelForm):
    class Meta:
        model = RAMDetails
        fields = ['capacity_gb', 'speed_mhz', 'ddr_type', 'module_count']

class StorageDetailsForm(forms.ModelForm):
    class Meta:
        model = StorageDetails
        fields = ['capacity_gb', 'storage_type', 'form_factor']

class MonitorDetailsForm(forms.ModelForm):
    class Meta:
        model = MonitorDetails
        fields = ['size_inch', 'resolution', 'refresh_rate_hz', 'panel_type']

class CoolingDetailsForm(forms.ModelForm):
    class Meta:
        model = CoolingDetails
        fields = ['cooling_type', 'fan_count']

class MotherboardDetailsForm(forms.ModelForm):
    class Meta:
        model = MotherboardDetails
        fields = ['chipset', 'socket_type', 'form_factor']

class PowerSupplyDetailsForm(forms.ModelForm):
    class Meta:
        model = PowerSupplyDetails
        fields = ['wattage', 'efficiency_rating', 'modular']

class CabinetDetailsForm(forms.ModelForm):
    class Meta:
        model = CabinetDetails
        fields = ['form_factor', 'color']

class AccessoryDetailsForm(forms.ModelForm):
    class Meta:
        model = AccessoryDetails
        fields = ['accessory_type', 'connection', 'color']