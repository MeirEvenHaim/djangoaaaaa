# C:\Users\meire\OneDrive\Desktop\backend - supermarket-template\myapp\Models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from paypal.standard.models import ST_PP_COMPLETED  # Payment completed status

from django.core.exceptions import ValidationError
    
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, related_name='Products', on_delete=models.CASCADE, db_index=True)
    supplier = models.ForeignKey(Supplier, related_name='Products', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Handle image uploads

    def __str__(self):
           return f"{self.name}" 

    
    
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='Cart', on_delete=models.CASCADE)  # Changed 'user' to 'client'
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False)  # Field to lock the cart after payment
    
   

    def __str__(self):
        return f"Cart of {self.user}, total price: {self.total_price}"


class Cart_link_product(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    # product_id = models.BigIntegerField(max_length=1_000_000_000, default = 0)
    product = models.ForeignKey(Product, related_name='Cart_link_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"user: {self.cart.user}, {self.quantity} of {self.product.name}"

from django.db import models

class Payment(models.Model):
    order_price = models.OneToOneField(
        Cart, on_delete=models.CASCADE, related_name='payment', blank=True, null=True,
        help_text="Links a payment to a specific cart order. This field is optional."
    )  
    
    # Payment identification
    paypal_order_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True,
        help_text="The unique ID for the PayPal order (e.g., '53325112R3150873A')."
    )
    capture_id = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="The unique ID for the payment capture (e.g., '1K3916117J273125C')."
    )

    # Payment details
    intent = models.CharField(
        max_length=50, default="CAPTURE", blank=True, null=True,
        help_text="The payment intent (e.g., 'CAPTURE')."
    )
    status = models.CharField(
        max_length=20, choices=[
            ('COMPLETED', 'Completed'),
            ('PENDING', 'Pending'),
            ('FAILED', 'Failed'),
        ],
        default='PENDING',
        help_text="The status of the payment.", blank=True, null=True,
    )
    currency = models.CharField(
        max_length=10, default="USD",
        help_text="The currency used for the payment.", blank=True, null=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        help_text="The total amount of the payment."
    )

    # Payer details
    payer_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Full name of the payer (e.g., 'meir evenhaim')."
    )
    payer_email = models.EmailField(
        blank=True, null=True,
        help_text="Email address of the payer."
    )
    payer_id = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="The unique ID of the payer."
    )

    # Shipping details
    shipping_address = models.JSONField(
        blank=True, null=True,
        help_text="The shipping address as a JSON object."
    )

    # Dates
    create_time = models.DateTimeField(
        blank=True, null=True,
        help_text="The creation time of the payment."
    )
    update_time = models.DateTimeField(
        blank=True, null=True,
        help_text="The last update time of the payment."
    )

    # Utility
    raw_response = models.JSONField(
        blank=True, null=True,
        help_text="Raw PayPal response for debugging or reference."
    )

    def __str__(self):
        return f"Payment {self.paypal_order_id} - {self.status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-create_time']

# Shipping Model
class Shipping(models.Model):
    cart_id = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='shipping')
    shipping_address = models.TextField()
    shipping_date = models.DateTimeField(blank=True, null=True)
    shipping_method = models.CharField(max_length=50, choices=[('Standard', 'Standard'), ('Express', 'Express')], default='Standard')
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Shipping {self.id} for Order {self.cart_id.id}"
