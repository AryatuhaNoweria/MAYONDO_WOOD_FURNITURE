from django import forms
from .models import StockEntry

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['product',
            'supplier',
            'quantity',
            'cost_price',
            'product_price',
            'quality',
            'color',
            'measurements',
        ]
        error_messages = {
            'product': {'required': 'please enter the Product .'},
            'supplier': {'required': 'please enter the supplier.'},
            'cost_price': {'required': 'please enter the Cost price .'},
            'product_price': {'required': 'please enter the Selling price .'},
            'quantity': {
                'required': ' please enter the quantity .',
                'invalid': 'Enter a valid number.'
            },
            'quality': {'required': 'please enter the quality'}
        }

    def clean_cost_price(self):
        cost_price = self.cleaned_data['cost_price']
        if cost_price < 0:
            raise forms.ValidationError("The cost price can't be lower than 0")
        return cost_price

    def clean_product_price(self):
        product_price = self.cleaned_data['product_price']
        if product_price < 0:
            raise forms.ValidationError("The selling price can't be lower than 0")
        return product_price

class StockQuantityUpdateForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }