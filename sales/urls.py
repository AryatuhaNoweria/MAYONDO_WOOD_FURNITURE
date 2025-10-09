from django.urls import path
from . import views

urlpatterns = [
    path('', views.sale_list, name='sale_list'),
    #path('add/', views.sale_form, name='add_sale'),
    path('create/', views.create_sale, name='create_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
   # path('edit/<int:pk>/', views.sale_form, name='edit_sale'),
    path('<int:pk>/delete/', views.delete_sale, name='delete_sale'),
    path('sales/<int:pk>/edit/', views.edit_sale, name='edit_sale'),
    path('record_sale/', views.record_sale, name='record_sale'),
    path('receipt/<int:sale_id>/', views.generate_receipt, name='generate_receipt'),
    path('sales_history/', views.sales_history, name='sales_history'),
    path('receipt/<int:sale_id>/download/', views.download_receipt_pdf, name='download_receipt_pdf'),
    path('record_sale/', views.record_sale, name='record_sale'),
     #path('receipt/<int:sale_id>/', users_views.receipt, name='receipt'),
]
