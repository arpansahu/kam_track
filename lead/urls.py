from django.urls import path
from lead.views import (
    LeadListView, LeadCreateView, LeadDetailView, LeadUpdateView,
    autocomplete_lead_name, autocomplete_company_name
)

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('add/', LeadCreateView.as_view(), name='lead-add'),
    path('<uuid:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<uuid:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),

    # Autocomplete Views
    path('autocomplete/lead-name/', autocomplete_lead_name, name='autocomplete-lead-name'),
    path('autocomplete/company-name/', autocomplete_company_name, name='autocomplete-company-name'),
]
