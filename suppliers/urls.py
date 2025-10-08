from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('add/', views.supplier_create, name='add_supplier'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('edit/<int:pk>/', views.supplier_update, name='edit_supplier'),
    path('<int:pk>/delete/', views.supplier_delete, name='delete_supplier'),
]