from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Define roles
    MANAGER = 'manager'
    ATTENDANT = 'attendant'
    SALES_AGENT = 'sales_agent'

    ROLE_CHOICES = [
        (MANAGER, 'Manager'),
        (ATTENDANT, 'Attendant'),
        (SALES_AGENT, 'Sales Agent'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ATTENDANT)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
