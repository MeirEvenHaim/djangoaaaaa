from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_payment_email(subject, message, recipient_list):
    send_mail(subject, message, 'your-email@gmail.com', recipient_list)
