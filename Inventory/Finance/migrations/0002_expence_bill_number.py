# Generated by Django 5.0.6 on 2024-10-22 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expence',
            name='bill_number',
            field=models.CharField(default='No Bill', max_length=20),
        ),
    ]