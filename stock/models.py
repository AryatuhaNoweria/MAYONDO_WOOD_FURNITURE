from django.db import models
from products.models import Product
from suppliers.models import Supplier
#from django.contrib.auth.models import User
from django.conf import settings
#create your models  here
class StockEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quality = models.CharField(max_length=50)
    color = models.CharField(max_length=30, blank=True, null=True)
    measurements = models.CharField(max_length=100, blank=True, null=True)
    date_received = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

class StockUpdate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    change_reason = models.CharField(max_length=100)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


