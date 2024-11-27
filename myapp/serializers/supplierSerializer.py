from rest_framework import serializers
from myapp.Models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_email', 'phone_number', 'address']  # Use the correct field names