from rest_framework import serializers
from myapp.Models import Cart, Cart_link_product, Payment, Product 
from myapp.services.stock_manager import StockManager


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart_link_product
        fields = ["id",'cart_id', 'product_id', 'quantity','product_name', 'client_name' ,"product_price" ]
        
    def get_id(self, obj):
        # Assuming the client name is stored in the `User` model in the `name` field
        return obj.id  # Adjust this if the name field is different
    
    def get_product_name(self, obj):
        return obj.product.name  # Retrieves the product name
    
    def get_product_price(self, obj):
        return obj.product.price  # Retrieves the product name

    def get_client_name(self, obj):
        return obj.cart.user.username  # Assumes `user` is the user related to the `cart`

    def validate(self, data):
        """
        Check that the requested quantity is available in stock and the user has permission.
        """
        cart = data.get('cart')
        product = data.get('product')
        quantity = data.get('quantity')
        user = self.context['request'].user

        if not user.is_staff and cart.user != user:
            raise serializers.ValidationError("You do not have permission to modify this cart.")

        if product.stock < quantity:
            raise serializers.ValidationError(f"Insufficient stock for {product.name}. Only {product.stock} available.")

        return data

    def create(self, validated_data):
        cart = validated_data['cart']
        product = validated_data['product']
        quantity = validated_data['quantity']
        
        # Use StockManager to handle adding to cart
        cart_item = StockManager.add_to_cart(cart, product.id, quantity)

        # Recalculate the total price for the cart
        self.calculate_total_price(cart)

        return cart_item
    
    def update(self, instance, validated_data):
        new_quantity = validated_data['quantity']
        product = instance.product
        old_quantity = instance.quantity

        # Calculate the difference in quantity
        quantity_difference = new_quantity - old_quantity

        # Check for sufficient stock if we're increasing the quantity
        if quantity_difference > 0:
            if product.stock < quantity_difference:
                raise serializers.ValidationError(f"Insufficient stock for {product.name}. Only {product.stock} available.")

        # Use StockManager to handle stock updates
        StockManager.update_cart_product(instance.id, new_quantity)

        # Update the cart item quantity and save
        instance.quantity = new_quantity
        instance.save()

        # Recalculate the total price for the cart
        self.calculate_total_price(instance.cart)

        return instance

    def calculate_total_price(self, cart):
        """
        Calculate the total price of the cart.
        """
        total = sum(item.product.price * item.quantity for item in cart.cart_items.all())
        cart.total_price = total
        cart.save()



class CartSerializer(serializers.ModelSerializer):
    # Define a custom field to display product names and quantities directly within the cart
    cart_link_product = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','locked', 'user', 'total_price', 'created_at', 'cart_link_product', 'client_name', 'payment_status']

    def get_client_name(self, obj):
        return obj.user.username  # Display the username of the cart owner

    def get_payment_status(self, obj):
        """
        If payment exists, return the status. Otherwise, provide a default message.
        """
        payment = Payment.objects.filter(order_price=obj).first()
        if payment:
            return payment.status
        else:
            return 'No payment initiated'

    def get_cart_link_product(self, obj):
        """
        Get the product name and quantity for each item in the cart.
        This field is populated without a new serializer, directly in the CartSerializer.
        """
        # Retrieve all cart items related to this cart
        cart_items = Cart_link_product.objects.filter(cart=obj)
        
        # Collect product name and quantity for each item in the cart
        product_info = []
        for item in cart_items:
            product_info.append({
                'product_name': item.product.name,
                'product_price': item.product.price,# Fetch the product name
                'quantity': item.quantity  # Fetch the quantity of that product in the cart
            })

        return product_info

    def create(self, validated_data):
        """
        When creating a new cart, you may want to initiate a PayPal transaction if no payment exists.
        """
        user = validated_data.get('user')
        cart = Cart.objects.create(user=user)
        
        return cart

    def update(self, instance, validated_data):
        """
        Update cart logic. You can include more logic here for payment or cart changes.
        """
        cart_link_products = validated_data.pop('cart_link_product', [])

        # Update cart details
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        # Update cart items
        existing_items = {item.product.id: item for item in instance.cart_link_product.all()}
        new_items = {item_data['product'].id: item_data for item_data in cart_link_products}

        for product_id, item in existing_items.items():
            if product_id not in new_items:
                item.delete()

        for product_id, item_data in new_items.items():
            if product_id in existing_items:
                item = existing_items[product_id]
                item.quantity = item_data['quantity']
                item.save()
            else:
                Cart_link_product.objects.create(cart=instance, **item_data)

        return instance