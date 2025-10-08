from django import forms
from .models import SalesReport, StockReport
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SalesReportForm(forms.ModelForm):
    class Meta:
        model = SalesReport
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('submit', 'Generate Sales Report'))

class StockReportForm(forms.ModelForm):
    class Meta:
        model = StockReport
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Generate Stock Report'))
