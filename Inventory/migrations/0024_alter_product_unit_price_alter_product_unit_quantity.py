# Generated by Django 5.0.6 on 2024-10-25 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0023_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]