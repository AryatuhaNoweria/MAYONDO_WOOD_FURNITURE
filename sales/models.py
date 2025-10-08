from django.db import models
from products.models import Product
from customers.models import Customer
#from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('overdraft', 'Bank Overdraft'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    sales_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transport_included = models.BooleanField(default=False)
    transport_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    final_amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    receipt_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
