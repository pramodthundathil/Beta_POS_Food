# Generated by Django 5.0.6 on 2024-10-18 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0006_order_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
