from django.core.exceptions import ValidationError
from django.db import transaction
from myapp.Models import Product, Cart_link_product
from rest_framework import serializers 

class StockManager:
        @staticmethod
        def check_stock(product, quantity):
            if product.stock < quantity:
                raise ValidationError(f"Insufficient stock for {product.name}. Only {product.stock} available.")

        @staticmethod
        def add_to_cart(cart, product_id, quantity):
            with transaction.atomic():
                product = Product.objects.get(id=product_id)  # Assuming you have a Product model
                
                # Check stock availability
                if product.stock < quantity:
                    raise serializers.ValidationError(f"Insufficient stock for {product.name}. Only {product.stock} available.")
                
                # Create a new cart item
                cart_product = Cart_link_product.objects.create(cart=cart, product=product, quantity=quantity)
                
                # Decrease the stock of the product
                product.stock -= quantity
                product.save()  # Save the updated stock

                return cart_product
        @staticmethod
        def update_cart_product(cart_product_id, new_quantity):
            with transaction.atomic():
                cart_product = Cart_link_product.objects.select_for_update().get(id=cart_product_id)
                product = cart_product.product

            # Calculate the quantity difference
            quantity_difference = new_quantity - cart_product.quantity

            # If increasing quantity, check stock availability
            if quantity_difference > 0:
                if product.stock < quantity_difference:
                    raise serializers.ValidationError(f"Insufficient stock for {product.name}. Only {product.stock} available.")
                product.stock -= quantity_difference  # Decrease stock
            elif quantity_difference < 0:
                # If decreasing quantity, return stock to inventory
                product.stock += abs(quantity_difference)  # Increase stock for returned quantity

            # Save the updated product stock
            product.save()
            # Update the cart product quantity
            cart_product.quantity = new_quantity  
            cart_product.save()  # Save the cart product

        @staticmethod
        def remove_from_cart(cart_product_id):
            with transaction.atomic():
                # Fetch the cart product with a lock for updating
                cart_product = Cart_link_product.objects.select_for_update().get(id=cart_product_id)
                product = cart_product.product
                
                # Return stock to the product based on the cart item's quantity
                product.stock += cart_product.quantity
                
                # Save the updated product stock
                product.save()
                
                # Delete the cart item
                cart_product.delete()