from rest_framework import serializers
from myapp.Models import Cart, Cart_link_product, Product
from myapp.services.stock_manager import StockManager
from django.contrib.auth.models import User
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    
    
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart_link_product
        fields = ["id",'cart', 'product', 'quantity','product_name', 'client_name']
        
    def get_id(self, obj):
        # Assuming the client name is stored in the `User` model in the `name` field
        return obj.cart_link_product.id  # Adjust this if the name field is different
    
    def get_product_name(self, obj):
        return obj.product.name  # Retrieves the product name

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
    cart_link_product = CartItemSerializer(many=True, required=False)
    client_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['user', "client_name", "cart_link_product", "created_at", "id", "total_price" , "client_name"]
        

    def get_client_name(self, obj):
        # Assuming the client name is stored in the `User` model in the `name` field
        return obj.user.username  # Adjust this if the name field is different

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user"].id)
        cart = Cart.objects.create(user_id=validated_data["user"].id)
        print(cart)
        return cart

    def update(self, instance, validated_data):
        cart_link_products = validated_data.pop('cart_link_product', [])

        instance.user_id = validated_data.get('user', instance.user_id)
        instance.save()

        existing_items = {item.product.id: item for item in instance.Cart_link_product.all()}
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