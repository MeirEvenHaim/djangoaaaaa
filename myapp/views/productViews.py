#productviews.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Product
from myapp.serializers.productSerializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from myapp.utils import get_or_set_cache, delete_cache
from django.db import connection
from django.conf import settings
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def creation_of_products_and_preview_products(request):
    if request.method == 'GET':
        def fetch_products_sp():
            with connection.cursor() as cursor:
                cursor.callproc('GetAllProducts')
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
            
            # Create a list of dictionaries (products), modifying the image URL
            products = [dict(zip(columns, row)) for row in rows]
            
            # Prepend the MEDIA_URL to the image path
            for product in products:
                product['image'] = settings.MEDIA_URL + product['image']
            
            return products

        cache_key = "all_products"
        products_data = get_or_set_cache(cache_key, fetch_products_sp, timeout=600)

        if products_data:
            return Response(products_data)
        else:
            return Response({"error": "Failed to fetch data"}, status=500)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def modifying_existing_products(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if not request.user.is_staff:
        return Response({"detail": "You do not have permission to perform this action."}, 
                        status=status.HTTP_403_FORBIDDEN)
        
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            delete_cache("all_products")  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE requests (delete product and invalidate cache)
    elif request.method == 'DELETE':
        product.delete()
        delete_cache("all_products")  # Invalidate products list cache
        return Response(status=status.HTTP_204_NO_CONTENT)






