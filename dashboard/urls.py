from django.urls import path
from dashboard.views import dashboard_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    # Dashboard does not need autocomplete endpoints in most cases unless filters for tasks/leads are added
]
