from django.urls import path
from .views import PerformanceReportListView, LeadReportSummaryView

urlpatterns = [
    path('performance-reports/', PerformanceReportListView.as_view(), name='performance-report-list'),
    path('lead-report-summary/', LeadReportSummaryView.as_view(), name='lead-report-summary'),
]
