from django.db import models
from lead.models import Lead
from kam_track.models import AbstractBaseModel

class Interaction(AbstractBaseModel):
    INTERACTION_TYPES = [
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('order', 'Order'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    details = models.TextField()  # Notes about the call, meeting, or order
    interaction_date = models.DateTimeField()  # Date and time of the interaction
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)  # For calls or meetings
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # For orders

    def __str__(self):
        return f"{self.get_interaction_type_display()} with {self.lead.account_name} on {self.interaction_date.strftime('%Y-%m-%d')}"

class Task(AbstractBaseModel):
    TASK_TYPES = [
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('follow-up', 'Follow-up'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    due_date = models.DateField()  # Date the task is due
    completed = models.BooleanField(default=False)  # Whether the task is completed

    def __str__(self):
        return f"{self.task_type} for {self.lead.account_name} on {self.due_date}"

class Note(AbstractBaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notes')
    interaction = models.ForeignKey(Interaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    content = models.TextField()  # Textual note content

    def __str__(self):
        return f"Note for {self.lead.account_name} (Interaction: {self.interaction})"

class Document(AbstractBaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='documents')
    interaction = models.ForeignKey(Interaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    uploaded_by = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Document uploaded by {self.uploaded_by.username} for {self.lead.account_name}"

