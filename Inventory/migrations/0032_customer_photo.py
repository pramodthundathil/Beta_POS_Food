# Generated by Django 5.0.6 on 2024-11-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0031_alter_vendor_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='Customer_photo'),
        ),
    ]
