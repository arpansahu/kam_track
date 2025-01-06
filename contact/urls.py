from django.urls import path
from .views import (
    ContactListView, ContactCreateView, ContactDetailView, ContactUpdateView, ContactDeleteView,
    autocomplete_contact_name, autocomplete_lead_name, autocomplete_role_name
)

urlpatterns = [
    path('', ContactListView.as_view(), name='contact-list'),
    path('add/', ContactCreateView.as_view(), name='contact-add'),
    path('<uuid:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('<uuid:pk>/update/', ContactUpdateView.as_view(), name='contact-update'),
    path('<uuid:pk>/delete/', ContactDeleteView.as_view(), name='contact-delete'),
    
    # Autocomplete Endpoints
    path('autocomplete/contact-name/', autocomplete_contact_name, name='autocomplete-contact-name'),
    path('autocomplete/contact-role/', autocomplete_role_name, name='autocomplete-contact-role'),
    path('autocomplete/lead-name/', autocomplete_lead_name, name='autocomplete-lead-name'),
]
