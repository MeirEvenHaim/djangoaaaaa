from django.contrib import admin
from .Models import (
    Category, Supplier, Product, Cart,
    Cart_link_product, Payment, Shipping
)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Display these columns in the list view
    search_fields = ('name',)  # Enable search by category name


# Supplier Admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone_number')
    search_fields = ('name', 'contact_email')  # Search by supplier name and email
    list_filter = ('name',)


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'supplier')
    list_filter = ('category', 'supplier')  # Filter by category and supplier
    search_fields = ('name',)  # Search by product name


# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_at', 'locked')
    list_filter = ('locked',)
    search_fields = ('user__username',)


# Cart Link Product Admin
@admin.register(Cart_link_product)
class CartLinkProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')


# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paypal_order_id', 'status', 'currency', 'amount', 'payer_email', 'create_time')
    search_fields = ('paypal_order_id', 'payer_email')
    list_filter = ('status', 'currency')


# Shipping Admin
@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'shipping_method', 'shipping_date', 'delivery_date')
    list_filter = ('shipping_method',)
    search_fields = ('cart_id__id',)
