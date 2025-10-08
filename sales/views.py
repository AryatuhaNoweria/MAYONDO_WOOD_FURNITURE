from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale
from .forms import SaleForm

# List all sales
def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sale_list.html', {'sale': sales})

# Add or Edit Sale
def sale_form(request, pk=None):
    if pk:
        sale = get_object_or_404(Sale, pk=pk)
    else:
        sale = None

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = SaleForm(instance=sale)

    return render(request, 'sale_form.html', {'form': form})

# View sale details
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sale})

# Delete a sale
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')
    return render(request, 'sale_confirm_delete.html', {'sale': sale})

def create_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.total_amount = 0  # Initialize total
            sale.save()

            total = 0
            for item in items:
                item.sale = sale
                item.save()
                total += item.quantity * item.price

            sale.total_amount = total
            sale.save()

            return redirect('sales_list')  # Redirect to sales list

    else:
        sale_form = SaleForm()
    return render(request, 'create_sale.html', {'sale_form': sale_form,})
