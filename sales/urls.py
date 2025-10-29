from django.urls import path
from . import views

urlpatterns = [
    path('', views.sale_list, name='sale_list'),

    # Sale creation
    path('create/', views.create_sale, name='create_sale'),

    # Sale detail and editing
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/edit/', views.edit_sale, name='edit_sale'),

    # Delete sale
    path('<int:pk>/delete/', views.delete_sale, name='delete_sale'),

    # Receipt view and PDF download
    path('receipt/<int:sale_id>/', views.receipt, name='receipt'),  # this was missing
    path('receipt/<int:sale_id>/download/', views.download_receipt_pdf, name='download_receipt_pdf'),

    # Sales history for logged-in user
    path('sales_history/', views.sales_history, name='sales_history'),
]
