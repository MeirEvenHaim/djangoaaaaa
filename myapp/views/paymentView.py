from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.Models import Payment,Cart
from myapp.serializers.payment_serializer import PaymentSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def create_payment(request):
    data = request.data
    
    # Check if order_price exists in the request data, if not, omit it
    if 'order_price' not in data or data['order_price'] is None:
        data['order_price'] = None  # or set it to a default value (if needed)
    
    # Optionally validate cart and payment amount consistency
    if data['order_price']:
        try:
            cart = Cart.objects.get(id=data['order_price'])
            if cart.locked:
                return Response({'error': 'This cart has already been locked for payment.'}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'error': 'Invalid cart ID provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Now serialize the data
    serializer = PaymentSerializer(data=data)
    if serializer.is_valid():
        payment = serializer.save()  # Save payment instance
        
        # Lock the cart after successful payment (if order_price was given)
        if payment.order_price:
            cart.locked = True
            cart.save()
            print("cart is locked")
        
        # Return success response with the payment data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Retrieve Payment
@api_view(['GET'])
def retrieve_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)

# List Payments
@api_view(['GET'])
def list_payments(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

# Update Payment
@api_view(['PUT'])
def update_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    serializer = PaymentSerializer(payment, data=request.data, partial=False)
    
    if serializer.is_valid():
        updated_payment = serializer.save()
        return Response(PaymentSerializer(updated_payment).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_payment_status(request, payment_id):
    try:
        # Fetch the payment instance by ID
        payment = Payment.objects.get(id=payment_id)
        
        # Get the status from the request data
        new_status = request.data.get('status')
        
        if new_status not in ['PENDING', 'COMPLETED', 'FAILED', 'CANCELED']:
            return Response({'error': 'Invalid status value provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # If status is 'CANCELED', unlock the cart
        if new_status == 'CANCELED' and payment.status == 'COMPLETED' and payment.order_price:
            cart = payment.order_price
            cart.locked = False
            cart.save()

        # Update the payment status
        payment.status = new_status
        payment.save()

        # Serialize and return the updated payment data
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
