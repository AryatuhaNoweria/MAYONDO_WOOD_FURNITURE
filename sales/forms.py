from django import forms
from .models import Sale, SaleItem
class SaleForm(forms.ModelForm):
    transport_included = forms.BooleanField(required=False, label="Include Transport (5% Fee)")
    class Meta:
        model = Sale
        fields = [
            'customer',
            'sales_agent',
            'total_amount',
            'transport_included',
            'transport_charge',
            'payment_type',
            'final_amount_paid',
            'receipt_number',
        ]
        error_messages = {
            'customer': {
                'required': "Please enter the customer's name.",
                'max_length': "Customer name is too long.",
            },
            'total_amount': {
                'required': "Please enter the total amount.",
            },
            'payment_type': {
                'required': "Please select a payment type.",
            },
            'sales_agent': {
                'required': "Please select the sales agent.",
            },
        }
    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get("total_amount")
        final_paid = cleaned_data.get("final_amount_paid")
        if total is not None and final_paid is not None:
            if final_paid > total:
                raise forms.ValidationError("Final amount paid cannot exceed total amount.")
            return cleaned_data   
        
class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price', 'subtotal']
        error_messages ={
            "product":{"required":"please enter the product"},
            "quantity":{"required":"please enter the quantity"},
            "unit_price":{"required":"please enter the unit_price"},
            "subtotal":{"required":"please enter the subtotal"}
        }

    def clean_subtotal(self):
        quantity = self.cleaned_data.get('quantity')
        unit_price = self.cleaned_data.get('unit_price')
        subtotal = self.cleaned_data.get('subtotal')
        if quantity is not None and unit_price is not None and subtotal is not None:
            expected_subtotal = quantity * unit_price
            if subtotal != expected_subtotal:
                raise forms.ValidationError(f"Subtotal should be {expected_subtotal}, but got {subtotal}.")
        return subtotal
    

