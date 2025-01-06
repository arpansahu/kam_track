from django.db import models
from contact.models import Contact
from kam_track.models import AbstractBaseModel

class Interaction(AbstractBaseModel):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=[('call', 'Call'), ('meeting', 'Meeting'), ('order', 'Order')])
    details = models.TextField()
    interaction_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_interaction_type_display()} with {self.contact.name} on {self.interaction_date.strftime('%Y-%m-%d')}"

class Order(AbstractBaseModel):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
        ('INR', 'Indian Rupees'),
        ('GBP', 'British Pounds'),
        ('AUD', 'Australian Dollars'),
    ]

    interaction = models.OneToOneField(Interaction, on_delete=models.CASCADE, related_name='order')
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')  # Currency field
    order_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending')

    def __str__(self):
        return f"Order for {self.interaction.contact.name} - Amount: {self.order_amount} {self.currency}"
