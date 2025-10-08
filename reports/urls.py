from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_report_pdf, name='sales_report'),
    path('stock/', views.stock_report_view, name='stock_report'),
]
