# Generated by Django 5.1 on 2025-01-06 11:35

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('locked', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_order_id', models.CharField(blank=True, help_text="The unique ID for the PayPal order (e.g., '53325112R3150873A').", max_length=255, null=True, unique=True)),
                ('capture_id', models.CharField(blank=True, help_text="The unique ID for the payment capture (e.g., '1K3916117J273125C').", max_length=255, null=True)),
                ('intent', models.CharField(blank=True, default='CAPTURE', help_text="The payment intent (e.g., 'CAPTURE').", max_length=50, null=True)),
                ('status', models.CharField(blank=True, choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('FAILED', 'Failed')], default='PENDING', help_text='The status of the payment.', max_length=20, null=True)),
                ('currency', models.CharField(blank=True, default='USD', help_text='The currency used for the payment.', max_length=10, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, help_text='The total amount of the payment.', max_digits=10, null=True)),
                ('payer_name', models.CharField(blank=True, help_text="Full name of the payer (e.g., 'meir evenhaim').", max_length=255, null=True)),
                ('payer_email', models.EmailField(blank=True, help_text='Email address of the payer.', max_length=254, null=True)),
                ('payer_id', models.CharField(blank=True, help_text='The unique ID of the payer.', max_length=255, null=True)),
                ('shipping_address', models.JSONField(blank=True, help_text='The shipping address as a JSON object.', null=True)),
                ('create_time', models.DateTimeField(blank=True, help_text='The creation time of the payment.', null=True)),
                ('update_time', models.DateTimeField(blank=True, help_text='The last update time of the payment.', null=True)),
                ('raw_response', models.JSONField(blank=True, help_text='Raw PayPal response for debugging or reference.', null=True)),
                ('order_price', models.OneToOneField(blank=True, help_text='Links a payment to a specific cart order. This field is optional.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='myapp.cart')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('stock', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='myapp.category')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Products', to='myapp.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Cart_link_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='myapp.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cart_link_product', to='myapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_address', models.TextField()),
                ('shipping_date', models.DateTimeField(blank=True, null=True)),
                ('shipping_method', models.CharField(choices=[('Standard', 'Standard'), ('Express', 'Express')], default='Standard', max_length=50)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('cart_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping', to='myapp.cart')),
            ],
        ),
    ]
