from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from .forms import SalesReportForm, StockReportForm
from .models import SalesReport, StockReport
from sales.models import Sale
from stock.models import StockEntry
# Create your views here.
@login_required
def sales_report_pdf(request):
    form = SalesReportForm(request.GET or None)
    sales = Sale.objects.all()
    total_sales = 0
    total_items_sold = 0
    transport_revenue = 0

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if start_date and end_date:
            sales = sales.filter(date__date__range=[start_date, end_date])
            total_sales = sales.aggregate(total=Sum('final_amount_paid'))['total'] or 0
            # Approximate items sold via SaleItem sum if related name exists; otherwise 0
            total_items_sold = 0
            transport_revenue = sales.filter(transport_included=True).aggregate(
                transport_sum=Sum('transport_charge')
            )['transport_sum'] or 0

            if 'submit' in request.GET:
                SalesReport.objects.create(
                    generated_by=request.user,
                    start_date=start_date,
                    end_date=end_date,
                    total_sales=total_sales,
                    total_items_sold=total_items_sold,
                    transport_revenue=transport_revenue,)

    context = {
        'form': form,
        'sales': sales,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
        'transport_revenue': transport_revenue,
    }
    return render(request, 'sales_report.html', context)


@login_required
def stock_report_view(request):
    form = StockReportForm(request.GET or None)
    stocks = StockEntry.objects.select_related('product', 'supplier').order_by('-date_received')
    notes = ''

    if form.is_valid():
        notes = form.cleaned_data.get('notes', '')

    context = {
        'form': form,
        'stocks': stocks,
        'notes': notes,
    }
    return render(request, 'stock_report.html', context)
