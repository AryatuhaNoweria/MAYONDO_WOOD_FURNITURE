from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name','company_name','phone','email','address']
        error_messages = {
            "name":{"required":"please enter the name"},
            "phone":{"required":"phone is required"},
            'address':{"required":"please enter address"}
            }
