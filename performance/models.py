from django.db import models
from lead.models import Lead
from kam_track.models import AbstractBaseModel

class PerformanceReport(AbstractBaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='performance_reports')
    report_date = models.DateField(auto_now_add=True)
    total_calls = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class LeadReportSummary(AbstractBaseModel):
    report_date = models.DateField()
    total_leads = models.PositiveIntegerField(default=0)
    converted_leads = models.PositiveIntegerField(default=0)
    lost_leads = models.PositiveIntegerField(default=0)
