from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Sum
from django.utils import timezone
from sales.models import Sale, SaleItem
from products.models import Product
from customers.models import Customer
from .forms import CustomUserCreationForm,Userloginform


def index_view(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = Userloginform(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if request.user.is_authenticated:
                if request.user.role =='manager':
                    return redirect ('manager_dashboard')
                if request.user.role =='sales_agent':
                    return redirect('sales_agent_dashboard')
                if request.user.role =='attendant':
                    return redirect('attendant_dashboard')
    else:
        form = Userloginform()
    context ={'form':form ,'hide_navbar': True}
    return render(request,'login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def manager_dashboard(request):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_revenue = Sale.objects.filter(date__gte=start_of_month).aggregate(
        total=Sum('final_amount_paid')
    )['total'] or 0
    total_sales = Sale.objects.filter(date__gte=start_of_month).count()
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    recent_sales = Sale.objects.select_related('customer').order_by('-date')[:5]
    low_stock = Product.objects.filter(current_stock__lte=5).order_by('current_stock')[:5]
    top_products = (
        SaleItem.objects.values('product__name')
        .annotate(quantity_sold=Sum('quantity'))
        .order_by('-quantity_sold')[:5]
    )

    context = {
        'kpi_total_revenue': total_revenue,
        'kpi_total_sales': total_sales,
        'kpi_total_customers': total_customers,
        'kpi_total_products': total_products,
        'recent_sales': recent_sales,
        'low_stock': low_stock,
        'top_products': top_products,
    }
    return render(request, 'manager_dashboard.html', context)

def attendant_dashboard(request):
    return render(request, 'attendant_dashboard.html')

def sales_dashboard(request):
    return render(request, 'sales_dashboard.html',{'hide_navbar': True})

