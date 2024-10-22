from django import forms
from .models import Product, Purchase
from .models import InventoryStock, PurchaseOrder




class InventoryStockForm(forms.ModelForm):
    class Meta:
        model = InventoryStock
        fields = [
            'product_name', 'product_stock', 'unit', 
            'min_stock_level', 'last_purchase_date', 
            'last_purchase_amount'
        ]
        
        widgets = {
            'product_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'product_name',
                    'placeholder': 'Enter product name',
                }
            ),
            'product_stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'product_stock',
                    'placeholder': 'Enter product stock',
                }
            ),
            'unit': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'unit',
                }
            ),
            'min_stock_level': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'min_stock_level',
                    'placeholder': 'Enter minimum stock level',
                }
            ),
            'last_purchase_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'id': 'last_purchase_date',
                    'type': 'date',
                }
            ),
            'last_purchase_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'last_purchase_amount',
                    'placeholder': 'Enter last purchase amount',
                }
            ),
        }


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = [
            'purchase_type', 'valid_till', 'supplier', 'place_of_supply', 
            'purchase_item','unit', 'quantity', 'purchase_price', 'discount', 'amount', 'order_status'
        ]
        
        widgets = {
            'purchase_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'purchase_type',
                }
            ),
            'valid_till': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'id': 'valid_till',
                    'type': 'date',  # To provide datetime picker
                }
            ),
            'supplier': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'supplier',
                }
            ),
            'place_of_supply': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'place_of_supply',
                    'placeholder': 'Enter place of supply',
                }
            ),
            'purchase_item': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'purchase_item',
                }
            ),
            'unit': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'unit',
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'quantity',
                    'placeholder': 'Enter quantity',
                }
            ),
            'purchase_price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'purchase_price',
                    'placeholder': 'Enter purchase price',
                }
            ),
            'discount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'discount',
                    'placeholder': 'Enter discount (%)',
                }
            ),
            
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'amount',
                    'placeholder': 'Enter total amount',
                }
            ),
            'order_status': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'order_status',
                }
            ),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'purchase_type', 'supplier', 'payment_terms', 'due_date', 'place_of_supply',
             'purchase_item', 'quantity',
            'purchase_price', 'discount', 'unit', 'amount', 'paid_amount', 
            'balance_amount', 'payment_status', 'shipping_cost', 'recived_date'
        ]
        widgets = {
            'purchase_type': forms.Select(attrs={'class': 'form-control', 'id': 'purchase_type'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'payment_terms': forms.NumberInput(attrs={'class': 'form-control', 'id': 'payment_terms'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'due_date', 'type': 'date'}),
            'place_of_supply': forms.TextInput(attrs={'class': 'form-control', 'id': 'place_of_supply'}),
            # 'purchase_order_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'purchase_order_number'}),
            # 'purchase_order_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'purchase_order_date', 'type': 'date'}),
            'purchase_item': forms.Select(attrs={'class': 'form-control', 'id': 'purchase_item'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'purchase_price'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'discount'}),
            'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit'}),
            # 'tax': forms.NumberInput(attrs={'class': 'form-control', 'id': 'tax'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'paid_amount'}),
            'balance_amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'balance_amount'}),
            'payment_status': forms.Select(attrs={'class': 'form-control', 'id': 'payment_status'}),
            'shipping_cost': forms.NumberInput(attrs={'class': 'form-control', 'id': 'shipping_cost'}),
            'recived_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'recived_date', 'type': 'date'}),
        }



from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'inventory', 'unit_price',"unit_quantity", 'Number_of_stock', 'unit', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'inventory': forms.Select(attrs={'class': 'form-control', 'id': 'inventory'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
            'unit_quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'unit_qantiry'}),
            'Number_of_stock': forms.NumberInput(attrs={'class': 'form-control', 'id': 'stock'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': 3}),
            'unit': forms.Select(attrs={'class': 'form-control', 'id': 'unit'}),
        }

