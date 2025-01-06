from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Interaction, Order
from contact.models import Contact
from lead.models import Lead
from .forms import CustomInteractionForm
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone


# Interaction List View
class InteractionListView(ListView):
    model = Interaction
    template_name = 'interaction/interaction-list.html'
    context_object_name = 'interactions'
    paginate_by = 10

    def get_queryset(self):
        return Interaction.objects.filter(is_deleted=False).order_by('-interaction_date')

# Interaction Create View
class InteractionCreateView(View):
    def get(self, request):
        contacts = Contact.objects.filter(contact_owner=request.user)
        interaction_type = request.GET.get('interaction_type', None)  # Get interaction type from URL query
        form = CustomInteractionForm(contacts_queryset=contacts, interaction_type_initial=interaction_type)
        return render(request, 'interaction/interaction_form.html', {'form': form})

    def post(self, request):
        form = CustomInteractionForm(request.POST, contacts_queryset=Contact.objects.filter(contact_owner=request.user))

        if form.is_valid():
            interaction = Interaction.objects.create(
                contact_id=form.cleaned_data['contact'],
                interaction_type=form.cleaned_data['interaction_type'],
                details=form.cleaned_data['details'],
                interaction_date=form.cleaned_data['interaction_date'],  # Expecting timezone-aware datetime
                duration_minutes=form.cleaned_data.get('duration_minutes'),
            )

            if form.cleaned_data['interaction_type'] == 'order':
                Order.objects.create(
                    interaction=interaction,
                    order_amount=form.cleaned_data['order_amount'],
                    currency=form.cleaned_data['currency'],
                )
                messages.success(request, "Order interaction created successfully!")
            else:
                messages.success(request, "Interaction created successfully!")

            return redirect('interaction-list')

        return render(request, 'interaction/interaction_form.html', {'form': form})


# Interaction Detail View
class InteractionDetailView(DetailView):
    model = Interaction
    template_name = 'interaction/interaction_detail.html'
    context_object_name = 'interaction'

# Interaction Update View
class InteractionUpdateView(UpdateView):
    model = Interaction
    # form_class = InteractionForm
    template_name = 'interaction/interaction_form.html'
    success_url = reverse_lazy('interaction-list')

    def form_valid(self, form):
        messages.success(self.request, "Interaction updated successfully!")
        return super().form_valid(form)

