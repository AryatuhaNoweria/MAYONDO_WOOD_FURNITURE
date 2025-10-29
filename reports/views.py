from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Sum
from .models import SalesReport, StockReport
from .forms import SalesReportFilterForm

def sales_report_view(request):
    form = SalesReportFilterForm(request.GET or None)
    sales = SalesReport.objects.all()

    # Apply filters
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        generated_by = form.cleaned_data.get('generated_by')

        if start_date and end_date:
            sales = sales.filter(start_date__gte=start_date, end_date__lte=end_date)
        if generated_by:
            sales = sales.filter(generated_by=generated_by)

    # Aggregated totals
    totals = sales.aggregate(
        total_sales=Sum('total_sales'),
        total_items_sold=Sum('total_items_sold'),
        transport_revenue=Sum('transport_revenue')
    )

    context = {
        'form': form,
        'sales': sales,
        'total_sales': totals['total_sales'] or 0,
        'total_items_sold': totals['total_items_sold'] or 0,
        'transport_revenue': totals['transport_revenue'] or 0,
    }
    return render(request, 'sales_report.html', context)


def stock_report_view(request):
    stock_reports = StockReport.objects.all().order_by('-date_generated')
    return render(request, 'stock_report.html', {'stock_reports': stock_reports})

def reports_home(request):
    return render(request, 'report_home.html')