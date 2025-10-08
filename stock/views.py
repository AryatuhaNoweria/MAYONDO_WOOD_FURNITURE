from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import StockEntry
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
    return render(request, 'delete_stock.html', {'stock': stock})
