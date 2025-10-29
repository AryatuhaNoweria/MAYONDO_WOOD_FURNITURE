from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','company_name','phone','email','address']
        error_messages ={
            "name":{"required":"please enter the name"},
            "phone":{"required":"please enter the phone"},
            "address":{"required":"please enter the address"}
        }
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) < 10:
            raise forms.ValidationError("Enter a valid phone number with at least 10 digits.")
        return phone
