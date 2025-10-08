from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_create, name='add_customer'),
    path('edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', views.customer_update, name='edit_customer'),
    path('<int:pk>/delete/', views.customer_delete, name='delete_customer'),
]
