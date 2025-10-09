from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Sale
from .forms import SaleForm
#from django.db.models import Sum, Count

def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sale_list.html', {'sales': sales})

def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.total_amount = 0  # optional logic
            sale.save()
            messages.success(request, "Sale added successfully!")
            return redirect('sale_list')
        else:
            messages.error(request, "Error: please check the form.")
    else:
        form = SaleForm()

    return render(request, 'create_sales.html', {'form': form})

def sale_detail(request, pk):
    sales= get_object_or_404(Sale, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sales})

def edit_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, "Sale updated successfully!")
            return redirect('sale_list')
        else:
            messages.error(request, "Error: please check your updates.")
    else:
        form = SaleForm(instance=sale)
    return render(request, 'edit_sale.html', {'form': form, 'sale': sale})

def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "Sale deleted successfully!")
        return redirect('sale_list')
    return render(request, 'sale_confirm_delete.html', {'sale': sale})


def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            transport_included = form.cleaned_data['transport_included']
            payment_type = form.cleaned_data['payment_type']

            transport_charge = Decimal('0.00')
            if transport_included:
                transport_charge = Decimal('0.00')  # Or calculate if needed

            # Create Sale object
            sale = Sale.objects.create(
                customer=customer,
                sales_agent=request.user,
                total_amount=0,  # Or calculate real total later
                transport_included=transport_included,
                transport_charge=transport_charge,
                payment_type=payment_type,
                final_amount_paid=0,  # Or calculate
                receipt_number=f"MWF-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )

            # Now you can safely redirect
            return redirect('receipt', sale_id=sale.id)
    else:
        form = SaleForm()

    return render(request, 'record_sale.html', {'form': form})



def generate_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'receipt.html', {'sale': sale})

def sales_history(request):
    sales = Sale.objects.filter(sales_agent=request.user).order_by('-date')
    return render(request, 'sale_history.html', {'sales': sales})


def download_receipt_pdf(request, sale_id):
    # Only allow managers and sales agents to download receipts
    if request.user.role not in ['manager', 'sales_agent']:
        messages.error(request, 'You do not have permission to download receipts.')
        return redirect('sales_dashboard')

    sale = get_object_or_404(Sale, id=sale_id)

    # Create HTTP response with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{sale.id}.pdf"'

    # Create a PDF object
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "MAYONDO WOOD AND FURNITURE LTD")

    # Subtitle
    p.setFont("Helvetica", 12)
    p.drawString(220, 780, "Sales Receipt")

    # Horizontal line
    p.line(50, 770, 550, 770)

    # Content details
    y = 740
    line_height = 22
    details = [
        ("Customer Name:", sale.customer_name),
        ("Product Name:", sale.product.name),
        ("Product Type:", sale.product.type),
        ("Quantity:", str(sale.quantity)),
        ("Payment Type:", sale.payment_type),
        ("Transport Needed:", "Yes (5% added)" if sale.transport_needed else "No"),
        ("Total Price (UGX):", str(sale.total_price)),
        ("Sales Agent:", sale.sales_agent.username),
        ("Date:", str(sale.sale_date)),
    ]

    for label, value in details:
        p.drawString(80, y, f"{label} {value}")
        y -= line_height

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(80, 120, "Thank you for doing business with Mayondo Wood and Furniture!")
    p.line(50, 110, 550, 110)
    p.drawString(230, 95, "Authorized Signature: __________________")

    # Finalize
    p.showPage()
    p.save()
    return response

def receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.items.all()  # all items in the sale
    return render(request, 'receipt.html', {'sale': sale, 'items': items})
