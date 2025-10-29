from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    transport_included = forms.BooleanField(required=False, label="Include Transport (5% Fee)")
    class Meta:
        model = Sale
        fields = [
            'customer',
            'product',
            'quantity',
            'unit_price',
            'sales_agent',
            'transport_included',
            'transport_charge',
            'payment_type',
            'total_amount_paid',
            'receipt_number'
        ]
        error_messages = {
            'customer': {'required': "Please enter the customer's name.",
                'max_length': "Customer name is too long."},
            'product':{"required":"please enter the product"},
            'unit_price': {'required': "Please enter the unit_price."},
            'total_amount_paid':{"required":"please enter the total_amount_paid"},
            'payment_type': {'required': "Please select a payment type."},
            'sales_agent': {'required': "Please select the sales agent."},
            'receipt_number' :{"required":"please enter the receipt_number"}
             

        }
    def clean_unit_price(self):
        unit_price= self.cleaned_data['unit_price']
        if unit_price < 0:
            raise forms.ValidationError("unit_price can not be less than 0")
        return unit_price   
    

    def clean_total_amount_paid(self):
        total_amount_paid= self.cleaned_data['total_amount_paid']
        if total_amount_paid < 0:
            raise forms.ValidationError("total_amount_paid can not be less than 0")
        return total_amount_paid