from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm

# LIST all customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customer': customers})


# DETAIL: View a single customer
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_detail.html', {'customer': customer})


# CREATE a new customer
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'customer_add.html', {'form': form,}) # Important: Let the template know it's an "add"
   


# UPDATE an existing customer
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_form.html', {'form': form, 'customer': customer})  # Important: So template knows it's an "edit"


# DELETE a customer
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    return render(request, 'customer_confirm_delete.html', {'customer': customer})


def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_edit.html', {'form': form})
