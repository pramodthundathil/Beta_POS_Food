from django import forms
from .models import Income, Expence

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['perticulers', 'amount', 'other']
        widgets = {
            'perticulers': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'income-perticulers',
                'placeholder': 'Enter particulars'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'income-amount',
                'placeholder': 'Enter amount'
            }),
            'other': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'income-other',
                'placeholder': 'Other details'
            }),
        }

class ExpenceForm(forms.ModelForm):
    class Meta:
        model = Expence
        fields = ['perticulers', 'amount', 'other']
        widgets = {
            'perticulers': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'expence-perticulers',
                'placeholder': 'Enter particulars'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'expence-amount',
                'placeholder': 'Enter amount'
            }),
            'other': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'expence-other',
                'placeholder': 'Other details'
            }),
        }
