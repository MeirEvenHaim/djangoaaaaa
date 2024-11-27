from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from myapp.Models import Cart_link_product
from myapp.serializers.cartSerializer import CartItemSerializer
from myapp.services.stock_manager import StockManager
from django.db import transaction

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def show_user_cart_and_create_user_cart(request):
    if request.method == 'GET':
        cart_items = Cart_link_product.objects.filter(cart__user=request.user) if not request.user.is_staff else Cart_link_product.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    cart_item = serializer.save()
                    return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def modify_user_cart_item(request, pk):
    cart_item = get_object_or_404(Cart_link_product, pk=pk)

    # Check if the user has permission to access this cart item
    if cart_item.cart.user != request.user and not request.user.is_staff:
        return Response({'error': 'You do not have permission to access this cart item.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CartItemSerializer(cart_item, data=request.data, context={'request': request})
        if serializer.is_valid():
            updated_cart_item = serializer.save()  # This will call the update method in the serializer
            return Response(CartItemSerializer(updated_cart_item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        StockManager.remove_from_cart(cart_item.id)  # Call the remove_from_cart method
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return 204 No Content on successful deletion