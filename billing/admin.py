from django.contrib import admin
from .models import *

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_name', 'email', 'is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'group', 'unit_price', 'stock']
    list_filter = ['brand', 'group']
    filter_horizontal = ['suppliers']

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    extra = 0; can_delete = False

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ['dni', 'last_name', 'first_name', 'email', 'saldo_efectivo', 'saldo_tarjeta']
=======
    list_display = ['dni', 'last_name', 'first_name', 'email']
>>>>>>> 72f4066fa5748c0921f8bba8fa79ee453233c999
    inlines = [CustomerProfileInline]

class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail; extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ['id', 'customer', 'user', 'metodo_pago', 'status', 'invoice_date', 'total']
    list_filter = ['metodo_pago', 'status']
=======
    list_display = ['id', 'customer', 'invoice_date', 'total']
>>>>>>> 72f4066fa5748c0921f8bba8fa79ee453233c999
    inlines = [InvoiceDetailInline]

