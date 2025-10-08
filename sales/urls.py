from django.urls import path
from . import views

urlpatterns = [
    path('', views.sale_list, name='sale_list'),
    path('add/', views.sale_form, name='add_sale'),
    path('edit/<int:pk>/', views.sale_form, name='edit_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('delete/<int:pk>/', views.sale_delete, name='delete_sale'),
]