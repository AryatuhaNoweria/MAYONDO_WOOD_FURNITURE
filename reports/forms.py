from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SalesReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    generated_by = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

