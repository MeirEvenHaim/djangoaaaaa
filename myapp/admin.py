# C:\Users\meire\OneDrive\Desktop\backend - supermarket-template\myapp\admin.py
from django.contrib import admin
from .Models import Category, Supplier, Product, Cart, Cart_link_product, Payment, Shipping
from django.utils.html import format_html

# Registering the Category model with customizations
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

# Registering the Supplier model with customizations
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone_number', 'address')
    search_fields = ('name', 'contact_email')
    list_filter = ('name',)

# Registering the Product model with custom display and image preview
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'supplier', 'image_preview')
    list_filter = ('category', 'supplier', 'price')
    search_fields = ('name', 'category__name', 'supplier__name')
    ordering = ('-price',)  # Orders by price descending
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Display a small image preview for product images."""
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

# Registering the Cart model with customizations
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

# Registering the Cart_link_product model
@admin.register(Cart_link_product)
class CartLinkProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart__user__username', 'product__name')
    search_fields = ('cart__user__username', 'product__name')

# Registering the Order model with detailed view
# Registering the Payment model with extensive search and filter options
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ( 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ( 'paypal_id')
    readonly_fields = ('payment_date',)
    ordering = ('-payment_date',)

# Registering the Shipping model with tracking information display
@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'shipping_address', 'shipping_method', 'tracking_number', 'delivery_date')
    list_filter = ('shipping_method',)
    search_fields = ('cart_id_user_name', 'tracking_number')
    readonly_fields = ('shipping_date',)
