from rest_framework import serializers
from myapp.Models import Shipping, Order

class ShippingSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())  # Reference the order

    class Meta:
        model = Shipping
        fields = ['id', 'order', 'shipping_address', 'shipping_date', 'tracking_number', 'shipping_method', 'delivery_date']

    def create(self, validated_data):
        shipping = Shipping.objects.create(**validated_data)
        return shipping
