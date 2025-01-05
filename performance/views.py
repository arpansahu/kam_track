from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import PerformanceReport, LeadReportSummary
from lead.models import Lead
from django.db.models import Avg, Sum

# Performance report list view
class PerformanceReportListView(ListView):
    model = PerformanceReport
    template_name = 'performance/performance_report_list.html'
    context_object_name = 'performance_reports'

    def get_queryset(self):
        return PerformanceReport.objects.filter(is_deleted=False).order_by('-report_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_leads'] = Lead.objects.count()
        context['total_orders'] = PerformanceReport.objects.aggregate(total_orders=Sum('total_orders'))['total_orders'] or 0
        context['avg_order_value'] = PerformanceReport.objects.aggregate(avg_order_value=Avg('avg_order_value'))['avg_order_value'] or 0
        return context


# Lead report summary view
class LeadReportSummaryView(ListView):
    model = LeadReportSummary
    template_name = 'performance/lead_report_summary.html'
    context_object_name = 'lead_summaries'

    def get_queryset(self):
        return LeadReportSummary.objects.filter(is_deleted=False).order_by('-report_date')
