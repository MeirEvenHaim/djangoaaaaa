# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from myapp.Models import Payment
# from django.conf import settings
# import paypalrestsdk
# from myapp.utils import logger


# # Helper function to update payment status in the database
# def update_payment_status(payment_id, status, refund_amount=None):
#     payment = Payment.objects.filter(paypal_id=payment_id).first()
#     if payment:
#         payment.status = status
#         if refund_amount:
#             payment.refund_amount = refund_amount
#         payment.save()
#         logger.info(f"Payment updated: {payment_id} - Status: {status}")
#         return True
#     return False


# # Payment Event Handlers
# def handle_authorization_created(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     return update_payment_status(payment_id, "Authorization Created")


# def handle_authorization_voided(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     return update_payment_status(payment_id, "Authorization Voided")


# def handle_capture_completed(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     return update_payment_status(payment_id, "Capture Completed")


# def handle_sale_completed(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     return update_payment_status(payment_id, "Completed")


# def handle_sale_denied(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     return update_payment_status(payment_id, "Denied")


# def handle_sale_pending(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     return update_payment_status(payment_id, "Pending")


# def handle_sale_refunded(resource):
#     payment_id = resource.get("parent_payment") or resource.get("id")
#     refund_amount = resource.get("amount", {}).get("total")
#     return update_payment_status(payment_id, "Refunded", refund_amount)


# # Checkout Event Handlers
# def handle_checkout_order_approved(resource):
#     order_id = resource.get("id")
#     logger.info(f"Checkout order approved: {order_id}")
#     return True


# def handle_checkout_order_completed(resource):
#     order_id = resource.get("id")
#     logger.info(f"Checkout order completed: {order_id}")
#     return True


# def handle_checkout_order_declined(resource):
#     order_id = resource.get("id")
#     logger.info(f"Checkout order declined: {order_id}")
#     return True


# def handle_checkout_order_saved(resource):
#     order_id = resource.get("id")
#     logger.info(f"Checkout order saved: {order_id}")
#     return True


# def handle_checkout_order_voided(resource):
#     order_id = resource.get("id")
#     logger.info(f"Checkout order voided: {order_id}")
#     return True


# # Dictionary mapping event types to handler functions
# EVENT_HANDLERS = {
#     "PAYMENT.AUTHORIZATION.CREATED": handle_authorization_created,
#     "PAYMENT.AUTHORIZATION.VOIDED": handle_authorization_voided,
#     "PAYMENT.CAPTURE.COMPLETED": handle_capture_completed,
#     "PAYMENT.SALE.COMPLETED": handle_sale_completed,
#     "PAYMENT.SALE.DENIED": handle_sale_denied,
#     "PAYMENT.SALE.PENDING": handle_sale_pending,
#     "PAYMENT.SALE.REFUNDED": handle_sale_refunded,
#     "CHECKOUT.ORDER.APPROVED": handle_checkout_order_approved,
#     "CHECKOUT.ORDER.COMPLETED": handle_checkout_order_completed,
#     "CHECKOUT.ORDER.DECLINED": handle_checkout_order_declined,
#     "CHECKOUT.ORDER.SAVED": handle_checkout_order_saved,
#     "CHECKOUT.ORDER.VOIDED": handle_checkout_order_voided,
# }


# @api_view(['POST'])
# def paypal_webhook(request):
#     event_body = request.data
#     event_type = event_body.get("event_type")
#     resource = event_body.get("resource", {})

#     try:
#         # Validate webhook signature before processing
#         if not validate_webhook(request, event_body):
#             logger.error("Invalid webhook signature.")
#             return Response({"error": "Invalid webhook signature"}, status=400)

#         # Handle the event using the event handler mapping
#         handler = EVENT_HANDLERS.get(event_type)
#         if handler:
#             if handler(resource):
#                 return Response({"message": f"{event_type} handled successfully"}, status=200)
#             else:
#                 logger.error(f"Failed to handle event: {event_type}")
#                 return Response({"error": "Failed to handle event"}, status=400)

#         logger.error(f"Unhandled event type: {event_type}")
#         return Response({"error": "Unhandled event type"}, status=400)

#     except Exception as e:
#         logger.error(f"Error processing PayPal webhook: {str(e)}")
#         return Response({"error": "Internal server error"}, status=500)


# def validate_webhook(request, event_body):
#     """
#     Verifies the webhook signature from PayPal to ensure authenticity.
#     """
#     headers = {
#         "auth_algo": request.headers.get("PayPal-Auth-Algo"),
#         "cert_url": request.headers.get("PayPal-Cert-Url"),
#         "transmission_id": request.headers.get("PayPal-Transmission-Id"),
#         "transmission_sig": request.headers.get("PayPal-Transmission-Sig"),
#         "transmission_time": request.headers.get("PayPal-Transmission-Time"),
#     }

#     try:
#         # Perform PayPal webhook signature validation
#         paypalrestsdk.WebhookEvent.verify(
#             transmission_id=headers["transmission_id"],
#             timestamp=headers["transmission_time"],
#             webhook_id=settings.PAYPAL_WEBHOOK_ID,
#             event_body=request.body.decode('utf-8'),
#             cert_url=headers["cert_url"],
#             actual_sig=headers["transmission_sig"],
#             auth_algo=headers["auth_algo"],
#         )
#         return True
#     except paypalrestsdk.ResourceNotFound as e:
#         logger.error(f"Invalid webhook signature: {str(e)}")
#         return False
