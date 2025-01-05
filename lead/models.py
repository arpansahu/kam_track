from account.models import Account
from kam_track.models import AbstractBaseModel
from django.db import models


class Lead(AbstractBaseModel):
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    STATUS_CHOICES = [('new', 'New'), ('contacted', 'Contacted'), ('in_progress', 'In Progress'), ('converted', 'Converted'), ('lost', 'Lost')]
    lead_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    assigned_kam = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.company_name})"

class Contact(AbstractBaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class Order(AbstractBaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('delivered', 'Delivered')])

class PerformanceMetric(AbstractBaseModel):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='performance_metrics')
    total_orders = models.PositiveIntegerField(default=0)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_order_date = models.DateField(blank=True, null=True)

class Activity(AbstractBaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=[('call', 'Call'), ('email', 'Email'), ('meeting', 'Meeting')])
    details = models.TextField(blank=True)
    activity_date = models.DateTimeField(auto_now_add=True)
