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
            'product': {'required': 'Product is required.'},
            'supplier': {'required': 'please enter the supplier.'},
            'cost_price': {'required': 'Cost price is required.'},
            'product_price': {'required': 'Selling price is required.'},
            'quantity': {
                'required': 'Quantity is required.',
                'invalid': 'Enter a valid number.'
            },
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
