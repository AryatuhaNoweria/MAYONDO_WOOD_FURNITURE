from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'type', 'category', 'description', 'color', 'measurements',
            'quality', 'product_price', 'cost_price', 'current_stock'
        ]
        error_messages ={
            "name":{"required" :"please enter the name"},
            "type":{"required":"please enter the type"},
            "category":{"required":"category is required"},
            "description":{"required":"please enter description"},
            "quality":{"required":"please enter the quality"},
            "product_price":{"required":"please enter product_price"},
            "cost_price":{"required":"please enter the cost_price"},
            "curent_stock":{"required":"please enter the current_stock"}
            
        }
    def clean_product_price(self):
        price = self.cleaned_data.get('product_price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price