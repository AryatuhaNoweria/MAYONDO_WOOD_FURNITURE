from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Sale
from .forms import SaleForm
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
    return render(request, 'delete_sale.html', {'sale': sale})
