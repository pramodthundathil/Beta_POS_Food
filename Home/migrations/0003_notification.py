# Generated by Django 5.0.6 on 2024-11-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_rename_date_of_give_staffsalary_date_of_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_heading', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ref_number', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]
