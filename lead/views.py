from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Lead
from .forms import LeadForm
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import JsonResponse
import logging

logger = logging.getLogger('django')

# List all leads
from django.utils.dateparse import parse_date

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'lead/lead-list.html'
    context_object_name = 'leads'
    paginate_by = 10

    def get_queryset(self):
        # Filter leads assigned to the current logged-in user (assigned KAM)
        queryset = Lead.objects.filter(assigned_kam=self.request.user, is_deleted=False).order_by('-created')
        lead_name = self.request.GET.get('lead_name', '')
        company_name = self.request.GET.get('company_name', '')
        status = self.request.GET.get('status', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        # Filter based on lead name
        if lead_name:
            queryset = queryset.filter(name__icontains=lead_name)

        # Filter based on company name
        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)

        # Filter based on status
        if status:
            queryset = queryset.filter(lead_status=status)

        # Filter based on date range
        if start_date:
            queryset = queryset.filter(created__date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created__date__lte=parse_date(end_date))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lead_name'] = self.request.GET.get('lead_name', '')
        context['company_name'] = self.request.GET.get('company_name', '')
        context['status'] = self.request.GET.get('status', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context

# Create a new lead
class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'lead/lead_form.html'
    success_url = reverse_lazy('lead-list')

    def form_valid(self, form):
        # Automatically set the current user as the assigned KAM
        form.instance.assigned_kam = self.request.user
        messages.success(self.request, "Lead created successfully!")
        return super().form_valid(form)

# Update lead details
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'lead/lead_form.html'
    success_url = reverse_lazy('lead-list')

    def get_queryset(self):
        # Only allow updates for leads assigned to the current KAM
        return Lead.objects.filter(assigned_kam=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Lead updated successfully!")
        return super().form_valid(form)


# Lead detail view
class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'lead/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        # Only show lead details if it belongs to the current KAM
        return Lead.objects.filter(assigned_kam=self.request.user)



# Autocomplete for Company Name
@login_required
def autocomplete_company_name(request):
    query = request.GET.get('company_name')
    logger.info(f"Searching Lead by Company {query}.")
    payload = []
    if query:
        # Filter leads by company name for the logged-in KAM
        leads = Lead.objects.filter(company_name__icontains=query, assigned_kam=request.user)
        for lead in leads:
            payload.append(lead.company_name)
    payload = list(set(payload))  # Remove duplicates
    return JsonResponse({'status': 200, 'data': payload})

# Autocomplete for Lead Name
@login_required
def autocomplete_lead_name(request):
    query = request.GET.get('lead_name')
    logger.info(f"Searching Lead by name {query}.")
    payload = []
    if query:
        # Filter leads by lead name for the logged-in KAM
        leads = Lead.objects.filter(name__icontains=query, assigned_kam=request.user)
        for lead in leads:
            payload.append(lead.name)
    payload = list(set(payload))  # Remove duplicates
    return JsonResponse({'status': 200, 'data': payload})