from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Sale
from .forms import SaleForm

# List all sales
def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sale_list.html', {'sales': sales})


# Create a new sale
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)

            # Calculate base total
            total_price = sale.unit_price * sale.quantity

            # Calculate transport charge (5%) if applicable
            if sale.transport_included:
                transport_fee = total_price * Decimal('0.05')
                sale.transport_charge = transport_fee
                total_price += transport_fee
            else:
                sale.transport_charge = Decimal('0.00')

            sale.total_amount_paid = total_price
            sale.sales_agent = request.user
            sale.receipt_number = f"MWF-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            sale.save()

            messages.success(request, "Sale added successfully!")
            return redirect('sale_list')
        else:
            messages.error(request, "Error: please check the form.")
    else:
        form = SaleForm()

    return render(request, 'create_sales.html', {'form': form})


# View a single sale detail
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sale})


# Edit an existing sale
def edit_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)

            total_price = sale.unit_price * sale.quantity
            if sale.transport_included:
                transport_fee = total_price * Decimal('0.05')
                sale.transport_charge = transport_fee
                total_price += transport_fee
            else:
                sale.transport_charge = Decimal('0.00')

            sale.total_amount_paid = total_price
            sale.save()

            messages.success(request, "Sale updated successfully!")
            return redirect('sale_list')
        else:
            messages.error(request, "Error: please check your updates.")
    else:
        form = SaleForm(instance=sale)
    return render(request, 'edit_sale.html', {'form': form, 'sale': sale})


# Delete a sale
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "Sale deleted successfully!")
        return redirect('sale_list')
    return render(request, 'sale_confirm_delete.html', {'sale': sale})


# View a sale receipt
def receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'receipt.html', {'sale': sale})


# Sales history for current user
def sales_history(request):
    sales = Sale.objects.filter(sales_agent=request.user).order_by('-date')
    return render(request, 'sale_history.html', {'sales': sales})


# Generate and download receipt as PDF
def download_receipt_pdf(request, sale_id):
    # Check permission (you need to have user roles set up)
    if not hasattr(request.user, 'role') or request.user.role not in ['manager', 'sales_agent']:
        messages.error(request, 'You do not have permission to download receipts.')
        return redirect('sale_list')

    sale = get_object_or_404(Sale, id=sale_id)

    # Prepare PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{sale.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title and header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(160, 800, "MAYONDO WOOD AND FURNITURE LTD")

    p.setFont("Helvetica", 12)
    p.drawString(250, 780, "Sales Receipt")
    p.line(50, 770, 550, 770)

    # Sale details
    y = 740
    line_height = 22

    details = [
        ("Customer Name:", sale.customer.name if sale.customer else "N/A"),
        ("Product Name:", sale.product.name),
        ("Quantity:", str(sale.quantity)),
        ("Unit Price:", f"{sale.unit_price}"),
        ("Payment Type:", sale.payment_type),
        ("Transport Included:", "Yes (5%)" if sale.transport_included else "No"),
        ("Transport Charge:", f"{sale.transport_charge}"),
        ("Total Paid:", f"{sale.total_amount_paid}"),
        ("Sales Agent:", sale.sales_agent.username if sale.sales_agent else "N/A"),
        ("Receipt Number:", sale.receipt_number),
        ("Date:", sale.date.strftime('%Y-%m-%d %H:%M')),
    ]

    for label, value in details:
        p.drawString(80, y, f"{label} {value}")
        y -= line_height

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(80, 120, "Thank you for doing business with Mayondo Wood and Furniture!")
    p.line(50, 110, 550, 110)
    p.drawString(230, 95, "Authorized Signature: __________________")

    p.showPage()
    p.save()

    return response
