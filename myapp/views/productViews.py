#productviews.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Product
from myapp.serializers.productSerializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from myapp.utils import get_or_set_cache, delete_cache


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def creation_of_products_and_preview_products(request):
    # Handle GET requests (cache products list)
    if request.method == 'GET':
        def fetch_products():
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return serializer.data
        
        # Use cache utility with a key
        cache_key = "all_products"
        products_data = get_or_set_cache(cache_key, fetch_products, timeout=600)
        return Response(products_data)
    
    # Handle POST requests (admins only, invalidate cache)
    elif request.method == 'POST':
        if request.user.is_staff:  # Ensure only admins can add products
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                delete_cache("all_products")  # Invalidate products list cache
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "You do not have permission to perform this action."}, 
                        status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def modifying_existing_products(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Retrieve the product
    
    # Handle GET requests (no caching for individual product details here)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # Only admins can update or delete products
    if not request.user.is_staff:
        return Response({"detail": "You do not have permission to perform this action."}, 
                        status=status.HTTP_403_FORBIDDEN)

    # Handle PUT requests (update product and invalidate cache)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            delete_cache("all_products")  # Invalidate products list cache
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE requests (delete product and invalidate cache)
    elif request.method == 'DELETE':
        product.delete()
        delete_cache("all_products")  # Invalidate products list cache
        return Response(status=status.HTTP_204_NO_CONTENT)