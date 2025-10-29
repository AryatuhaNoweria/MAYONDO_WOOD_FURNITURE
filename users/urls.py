from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/attendant/', views.attendant_dashboard, name='attendant_dashboard'),
    path('dashboard/sales/', views.sales_dashboard, name='sales_agent_dashboard'),
]
