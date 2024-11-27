from rest_framework import serializers
from myapp.Models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', "order_price","currency", 'payment_date', 'amount_payed', 'payment_method', 'paypal_id', 'status']

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment
