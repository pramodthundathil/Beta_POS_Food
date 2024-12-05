# Generated by Django 5.0.6 on 2024-12-02 05:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0033_rename_photo_customer_customer_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='tax',
            new_name='total_amount_before_discount',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='purchase_item',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='purchase_price',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='unit',
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_confirmation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='save_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='total_discount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='balance_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='discount',
            field=models.FloatField(blank=True, default=0, help_text='in %', null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='paid_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='place_of_supply',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='purchase_item',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='quantity',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='cess',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('Active', 'Active'), ('Expired', 'Expired')], default='Active', max_length=30),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='place_of_supply',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='valid_till',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='PurchaseItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('total_price', models.FloatField(editable=False)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventorys', to='Inventory.inventorystock')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_bill', to='Inventory.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('total_price', models.FloatField(editable=False)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_items', to='Inventory.inventorystock')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order_items', to='Inventory.purchaseorder')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_item',
            field=models.ManyToManyField(to='Inventory.inventorystock'),
        ),
    ]