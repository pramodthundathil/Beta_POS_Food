# Generated by Django 5.0.6 on 2024-10-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0007_orderitem_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='save_status',
            field=models.BooleanField(default=False),
        ),
    ]
