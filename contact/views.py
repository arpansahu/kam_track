from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Contact
from django.http import JsonResponse
from lead.models import Lead
from .forms import ContactForm
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


logger = logging.getLogger('django')

# List all contacts
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contact/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Contact.objects.filter(contact_owner=self.request.user)
        contact_name = self.request.GET.get('contact_name', '')
        role = self.request.GET.get('role', '')
        lead_name = self.request.GET.get('lead_name', '')

        # Filter based on search inputs
        if contact_name:
            queryset = queryset.filter(name__icontains=contact_name)
        if role:
            queryset = queryset.filter(role__icontains=role)
        if lead_name:
            queryset = queryset.filter(lead__name__icontains=lead_name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search filters back to the context for rendering in the template
        context['contact_name'] = self.request.GET.get('contact_name', '')
        context['role'] = self.request.GET.get('role', '')
        context['lead_name'] = self.request.GET.get('lead_name', '')
        return context


# Detail view for a contact
class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contact/contact_detail.html'
    context_object_name = 'contact'

    def get_queryset(self):
        # Restrict to contacts owned by the logged-in user
        return Contact.objects.filter(contact_owner=self.request.user)


# Create a new contact
class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = reverse_lazy('contact-list')

    def form_valid(self, form):
        form.instance.contact_owner = self.request.user  # Set contact owner to current user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


# Update contact details
class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = reverse_lazy('contact-list')

    def get_queryset(self):
        # Restrict updates to contacts owned by the logged-in user
        return Contact.objects.filter(contact_owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


# Delete contact
@login_required
@require_POST  # Ensure only POST requests are accepted
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, contact_owner=request.user)
    contact.delete()
    return JsonResponse({'status': 'success', 'message': 'Contact deleted successfully'}, status=200)
        
# Autocomplete for Contact Name
@login_required
def autocomplete_contact_name(request):
    query = request.GET.get('contact_name')
    logger.info(f"Searching Contact by name {query}.")
    payload = []
    if query:
        contacts = Contact.objects.filter(name__icontains=query, contact_owner=request.user)
        for objs in contacts:
            payload.append(objs.name)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})

# Autocomplete for Role Name
@login_required
def autocomplete_role_name(request):
    query = request.GET.get('role')
    logger.info(f"Searching Contact by role {query}.")
    payload = []
    if query:
        contacts = Contact.objects.filter(role__icontains=query, contact_owner=request.user)
        for objs in contacts:
            payload.append(objs.role)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})

# Autocomplete for Lead Name
@login_required
def autocomplete_lead_name(request):
    query = request.GET.get('lead_name')
    logger.info(f"Searching Contact by role {query}.")
    payload = []
    if query:
        contacts = Contact.objects.filter(lead__name__icontains=query, contact_owner=request.user)
        for objs in contacts:
            payload.append(objs.lead.name)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})