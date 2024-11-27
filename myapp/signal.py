# signals.py

from django.conf import settings
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .Models import Payment

@receiver(valid_ipn_received)
def handle_paypal_payment(sender, **kwargs):
    ipn_obj = sender

    # Ensure the payment is to the correct receiver
    if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
        return

    try:
        # Get the payment by ID (assuming you used payment.id as the invoice)
        payment = Payment.objects.get(id=ipn_obj.invoice)

        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # Mark payment as completed
            payment.complete_payment(ipn_obj.txn_id)
        else:
            # Optionally handle other statuses
            payment.status = 'Failed'
            payment.save()

    except Payment.DoesNotExist:
        # Handle the case where no matching payment is found
        pass
