from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from myapp.Models import Payment
from myapp.serializers.payment_serializer import PaymentSerializer
import paypalrestsdk # type: ignore
from django.conf import settings
from django.core.mail import send_mail

# Configure PayPal SDK
def get_paypal_client():
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_ENVIRONMENT,  # "sandbox" or "live"
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })
    return paypalrestsdk


@api_view(['GET', 'POST'])
def Payment_creation(request):
    """List all payments or create a new payment."""
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # PayPal Payment Creation
            amount = serializer.validated_data["amount"]
            currency = serializer.validated_data["currency"]

            paypal_payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [{
                    "amount": {"total": str(amount), "currency": currency},
                    "description": f"Payment for order ID {serializer.validated_data['order_price'].id}"
                }],
                "redirect_urls": {
                    "return_url": "http://localhost:8000/payment/success",
                    "cancel_url": "http://localhost:8000/payment/cancel"
                }
            })

            if paypal_payment.create():
                # Save the payment as pending
                payment = serializer.save(status="Pending")
                send_mail(
                subject="Payment Successful",
                message=f"Your payment for {payment.amount} {payment.currency} has been completed successfully.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["user@example.com"])
                return Response({
                    "payment_id": payment.id,
                    "paypal_url": paypal_payment.links[1].href  # Approval URL
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": paypal_payment.error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def Payment_modifications(request, pk):
    """Retrieve, update, or delete a payment."""
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            updated_payment = serializer.save()
            return Response(PaymentSerializer(updated_payment).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if payment.status != "Completed":
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Cannot delete a completed payment"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Payment_success(request):
    """Handle successful payment callbacks."""
    payment_id = request.data.get("payment_id")
    payer_id = request.data.get("payer_id")

    try:
        paypal_payment = paypalrestsdk.Payment.find(payment_id)
        if paypal_payment.execute({"payer_id": payer_id}):
            # Find and update the local payment record
            local_payment = Payment.objects.get(paypal_id=payment_id)
            local_payment.complete_payment(txn_id=payment_id, amount=paypal_payment.transactions[0].amount.total)
            return Response({"message": "Payment completed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": paypal_payment.error}, status=status.HTTP_400_BAD_REQUEST)

    except Payment.DoesNotExist:
        return Response({"error": "Local payment record not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Payment_cancel(request):
    """Handle payment cancellations."""
    payment_id = request.query_params.get("paymentId", None)

    if payment_id:
        # Optionally, log or find the payment and update its status
        try:
            payment = Payment.objects.get(paypal_id=payment_id)
            payment.status = "Cancelled"
            payment.save()

            # Send cancellation notification email
            send_mail(
                    subject="Payment Cancelled",
                    message=f"Your payment with ID {payment_id} has been cancelled.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[payment.order_price.user.email]  # Adjust if user model is different
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": "Payment was cancelled by the user."}, status=status.HTTP_200_OK)