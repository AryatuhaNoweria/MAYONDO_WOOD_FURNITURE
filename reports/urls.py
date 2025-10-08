from django.urls import path
from .views import sales_report_view, stock_report_view

urlpatterns = [
    path('sales/', sales_report_view, name='sales_report'),
    path('stock/', stock_report_view, name='stock_report'),
]
