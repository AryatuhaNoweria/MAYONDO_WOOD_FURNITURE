from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name
