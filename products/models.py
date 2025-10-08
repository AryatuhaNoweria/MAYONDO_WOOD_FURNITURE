from django.db import models
# Create your models here.
class Product(models.Model):
    WOOD = 'wood'
    FURNITURE = 'furniture'
    PRODUCT_TYPE_CHOICES = [
        (WOOD, 'Wood'),
        (FURNITURE, 'Furniture'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    category = models.CharField(max_length=50)  # e.g., sofa, timber
    description = models.TextField(blank=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    measurements = models.CharField(max_length=100, blank=True, null=True)
    quality = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
