from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def PayPal_webhook(request):
    event_body = request.data
    event_type = event_body.get("event_type")

    if event_type == "PAYMENT.SALE.COMPLETED":
        payment_id = event_body["resource"]["parent_payment"]
        # Find and update the payment in the database
        try:
            payment = Payment.objects.get(paypal_id=payment_id)
            payment.status = "Completed"
            payment.save()
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        return Response({"message": "Payment completed successfully"}, status=200)

    return Response({"error": "Unhandled event type"}, status=400)
