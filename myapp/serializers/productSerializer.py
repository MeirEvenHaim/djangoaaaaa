from rest_framework import serializers
from myapp.Models import Product, Supplier, Category
from rest_framework import serializers
from myapp.Models import Product, Supplier, Category

class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField(source='supplier.name', read_only=True)
    category = serializers.StringRelatedField(source='category.name', read_only=True)

    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source='supplier',
        write_only=True,
        required=True  # Make this field required
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=True  # Make this field required
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'supplier_id', 'category_id', 'supplier', 'category', 'image']
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'stock': {'required': True},
        }

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)  # Create product directly from validated data
        return product

    def update(self, instance, validated_data):
        # Update the product instance with the provided validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
