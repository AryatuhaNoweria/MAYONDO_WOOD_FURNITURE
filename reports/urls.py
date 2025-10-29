from django.urls import path
from . import views
from .views import sales_report_view

urlpatterns = [
    path('', views.reports_home, name='reports_home'),  # <== This line fixes the issue!
    #path('sales-report/', views.sales_report_pdf, name='sales_report'),
    path('stock-report/', views.stock_report_view, name='stock_report'),
    path('sales-report/', sales_report_view, name='sales_report'),
]


