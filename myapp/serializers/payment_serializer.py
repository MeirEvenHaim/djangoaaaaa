from rest_framework import serializers
from myapp.Models import Payment, Cart

class PaymentSerializer(serializers.ModelSerializer):
    
    # Make sure order_price is optional and can be null
    order_price = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), required=False, allow_null=True)

    # Add custom validation for amount
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be a positive value.")
        return value

    # Validate PayPal Order ID format
    def validate_paypal_order_id(self, value):
        if value and len(value) < 10:
            raise serializers.ValidationError("Invalid PayPal Order ID format.")
        return value

    # Custom validation for status
    def validate_status(self, value):
        valid_statuses = ['COMPLETED', 'PENDING', 'FAILED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}.")
        return value

    # Optionally format create_time and update_time to a more readable format
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.create_time:
            representation['create_time'] = instance.create_time.strftime('%Y-%m-%d %H:%M:%S')
        if instance.update_time:
            representation['update_time'] = instance.update_time.strftime('%Y-%m-%d %H:%M:%S')
        return representation

    class Meta:
        model = Payment
        fields = [
            'id', 
            'order_price', 
            'paypal_order_id', 
            'capture_id', 
            'intent', 
            'status', 
            'currency', 
            'amount', 
            'payer_name', 
            'payer_email', 
            'payer_id', 
            'shipping_address', 
            'create_time', 
            'update_time', 
            'raw_response',
        ]
        read_only_fields = ['create_time', 'update_time']
        extra_kwargs = {
            'order_price': {'required': False, 'allow_null': True},  # Make order_price truly optional
            'paypal_order_id': {'required': False},  # Optional if not provided in the request
        }