from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
# create your model here


class SalesReport(models.Model):
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_items_sold = models.PositiveIntegerField()
    transport_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

class StockReport(models.Model):
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_generated = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

