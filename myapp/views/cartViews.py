from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Cart
from myapp.serializers.cartSerializer import CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Show_cart_and_create_cart(request):
    if request.method == 'GET':
        if request.user.is_staff:
            carts = Cart.objects.all()
        else:
            carts = Cart.objects.filter(user_id=request.user.id)

        serializer = CartSerializer(carts, many=True)
        print(f"serializer.data: {serializer}")
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = CartSerializer(data=request.data)
        if request.user.is_staff:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # For clients, automatically set the user as the current client
        else:
            if serializer.is_valid():
                serializer.save(user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def Show_cart_and_modify_cart(request, pk):
    cart = get_object_or_404(Cart, pk=pk)

    if request.user.is_staff:
        if request.method == 'GET':
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CartSerializer(cart, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        if cart.user_id != request.user.id:
            raise ValidationError("You can only modify or delete your own cart.")

        if request.method == 'GET':
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CartSerializer(cart, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)