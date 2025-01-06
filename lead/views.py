from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Lead
from .forms import LeadForm
from account.models import Account


from django.http import JsonResponse


# List all leads
class LeadListView(ListView):
    model = Lead
    template_name = 'lead/lead-list.html'
    context_object_name = 'leads'
    paginate_by = 10

    def get_queryset(self):
        return Lead.objects.filter(is_deleted=False, ).order_by('-created')


# Create a new lead
class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'lead/lead_form.html'
    success_url = reverse_lazy('lead-list')

    def form_valid(self, form):
        form.instance.assigned_kam = self.request.user
        messages.success(self.request, "Lead created successfully!")
        return super().form_valid(form)


# Update lead details
class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'lead/lead_form.html'
    success_url = reverse_lazy('lead-list')

    def form_valid(self, form):
        messages.success(self.request, "Lead updated successfully!")
        return super().form_valid(form)


# Lead detail view
class LeadDetailView(DetailView):
    model = Lead
    template_name = 'lead/lead_detail.html'
    context_object_name = 'lead'


def autocomplete_lead_name(request):
    query = request.GET.get('lead_name', '')
    leads = Lead.objects.filter(name__icontains=query)
    results = [{'id': lead.id, 'name': lead.name} for lead in leads]
    return JsonResponse({'data': results})

def autocomplete_company_name(request):
    query = request.GET.get('company_name', '')
    leads = Lead.objects.filter(company_name__icontains=query)
    results = [{'id': lead.id, 'company_name': lead.company_name} for lead in leads]
    return JsonResponse({'data': results})

def autocomplete_kam_name(request):
    query = request.GET.get('assigned_kam', '')
    users = Account.objects.filter(username__icontains=query, role='kam')
    results = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse({'data': results})
