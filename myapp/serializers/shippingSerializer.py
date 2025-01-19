from rest_framework import serializers
from myapp.Models import Shipping,Cart

class ShippingSerializer(serializers.ModelSerializer):
    # Assuming cart_id is the foreign key field, use the correct field name
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())  # Reference to the Cart model

    class Meta:
        model = Shipping
        fields = ['id', 'cart_id', 'shipping_address', 'shipping_date', 'shipping_method', 'delivery_date']
        # Note: I removed 'tracking_number' since it's not defined in the Shipping model in your example.

    def create(self, validated_data):
        # Create a Shipping instance using validated data
        shipping = Shipping.objects.create(**validated_data)
        return shipping
