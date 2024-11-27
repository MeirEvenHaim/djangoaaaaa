from django.test import TestCase
from myapp.tasks import send_payment_email

class CeleryTestCase(TestCase):
    def test_send_payment_email(self):
        result = send_payment_email.delay("Test Subject", "Test Message", ["user@example.com"])
        self.assertTrue(result.successful())
