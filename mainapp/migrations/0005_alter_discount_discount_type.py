# Generated by Django 5.2 on 2025-04-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount_type',
            field=models.CharField(choices=[('cart', 'Cart'), ('delivery', 'Delivery-specific')], max_length=10),
        ),
    ]
