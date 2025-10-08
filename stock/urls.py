from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('add/', views.add_stock, name='add_stock'),
    path('edit/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('delete/<int:pk>/', views.delete_stock, name='delete_stock'),
]
