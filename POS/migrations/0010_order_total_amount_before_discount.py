# Generated by Django 5.0.6 on 2024-10-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0009_order_sales_man'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_amount_before_discount',
            field=models.FloatField(default=0),
        ),
    ]
