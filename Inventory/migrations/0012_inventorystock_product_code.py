# Generated by Django 5.0.6 on 2024-10-14 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0011_inventorystock_purchaseorder_purchase_order_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorystock',
            name='product_code',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
