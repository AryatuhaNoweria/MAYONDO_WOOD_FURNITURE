from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import StockEntry, StockUpdate
from .forms import StockEntryForm

def stock_list(request):
    stocks = StockEntry.objects.all()
    return render(request, 'stock_list.html', {'stock': stocks})

def add_stock(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock added successfully!')
            return redirect('stock_list')
    else:
        form = StockEntryForm()
    return render(request, 'add_stock.html', {'form': form})

def edit_stock(request, pk):
    stock = get_object_or_404(StockEntry, pk=pk)
    if request.method == 'POST':
        form = StockEntryForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('stock_list')
    else:
        form = StockEntryForm(instance=stock)
    return render(request, 'edit_stock.html', {'form': form})

def delete_stock(request, pk):
    stock = get_object_or_404(StockEntry, pk=pk)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Stock deleted successfully!')
        return redirect('stock_list')
    return render(request, 'stock_confirm_delete.html', {'stock': stock})

def update_stock(request, stock_id):
    stock_entry = get_object_or_404(StockEntry, pk=stock_id)
    old_quantity = stock_entry.quantity

    if request.method == 'POST':
        form = StockQuantityUpdateForm(request.POST, instance=stock_entry)
        if form.is_valid():
            updated_entry = form.save(commit=False)
            new_quantity = updated_entry.quantity

            # Only log the change if quantity has changed
            if new_quantity != old_quantity:
                updated_entry.save()

                # Create StockUpdate record
                StockUpdate.objects.create(
                    product=stock_entry.product,
                    old_quantity=old_quantity,
                    new_quantity=new_quantity,
                    change_reason=request.POST.get('change_reason', 'Updated by user'),
                    updated_by=request.user,
                )

                return redirect('view_stock')  # Or wherever you list stock
    else:
        form = StockQuantityUpdateForm(instance=stock_entry)

    return render(request, 'update_stock.html', {'form': form, 'stock_entry': stock_entry})