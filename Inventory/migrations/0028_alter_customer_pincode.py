# Generated by Django 5.0.6 on 2024-11-01 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0027_product_barcode_number_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pincode',
            field=models.CharField(max_length=100),
        ),
    ]
