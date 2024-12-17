# Generated by Django 5.1 on 2024-12-17 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_payment_options_alter_payment_amount_payed_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-create_time'], 'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='amount_payed',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_metadata',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='paypal_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='transaction_fee',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='The total amount of the payment.', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='capture_id',
            field=models.CharField(blank=True, help_text="The unique ID for the payment capture (e.g., '1K3916117J273125C').", max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='create_time',
            field=models.DateTimeField(blank=True, help_text='The creation time of the payment.', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='intent',
            field=models.CharField(blank=True, default='CAPTURE', help_text="The payment intent (e.g., 'CAPTURE').", max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payer_id',
            field=models.CharField(blank=True, help_text='The unique ID of the payer.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='paypal_order_id',
            field=models.CharField(blank=True, help_text="The unique ID for the PayPal order (e.g., '53325112R3150873A').", max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='raw_response',
            field=models.JSONField(blank=True, help_text='Raw PayPal response for debugging or reference.', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='shipping_address',
            field=models.JSONField(blank=True, help_text='The shipping address as a JSON object.', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='update_time',
            field=models.DateTimeField(blank=True, help_text='The last update time of the payment.', null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(blank=True, default='USD', help_text='The currency used for the payment.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payer_name',
            field=models.CharField(blank=True, help_text="Full name of the payer (e.g., 'meir evenhaim').", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('FAILED', 'Failed')], default='PENDING', help_text='The status of the payment.', max_length=20, null=True),
        ),
    ]