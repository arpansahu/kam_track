from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Interaction, Task, Note, Document
from lead.models import Lead
from .forms import InteractionForm, TaskForm, NoteForm, DocumentForm
from django.http import JsonResponse
from django.db.models import Q

# Interaction List View
class InteractionListView(ListView):
    model = Interaction
    template_name = 'interaction/interaction_list.html'
    context_object_name = 'interactions'
    paginate_by = 10

    def get_queryset(self):
        return Interaction.objects.filter(is_deleted=False).order_by('-interaction_date')

# Interaction Create View
class InteractionCreateView(CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = 'interaction/interaction_form.html'
    success_url = reverse_lazy('interaction-list')

    def form_valid(self, form):
        lead_id = self.kwargs.get('lead_id')
        lead = get_object_or_404(Lead, id=lead_id)
        form.instance.lead = lead
        messages.success(self.request, "Interaction created successfully!")
        return super().form_valid(form)

# Interaction Detail View
class InteractionDetailView(DetailView):
    model = Interaction
    template_name = 'interaction/interaction_detail.html'
    context_object_name = 'interaction'

# Interaction Update View
class InteractionUpdateView(UpdateView):
    model = Interaction
    form_class = InteractionForm
    template_name = 'interaction/interaction_form.html'
    success_url = reverse_lazy('interaction-list')

    def form_valid(self, form):
        messages.success(self.request, "Interaction updated successfully!")
        return super().form_valid(form)

# Task List and Create Views
class TaskListView(ListView):
    model = Task
    template_name = 'interaction/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_deleted=False, completed=False).order_by('due_date')

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'interaction/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        lead_id = self.kwargs.get('lead_id')
        lead = get_object_or_404(Lead, id=lead_id)
        form.instance.lead = lead
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)

# Note Create View
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'interaction/note_form.html'

    def form_valid(self, form):
        lead_id = self.kwargs.get('lead_id')
        interaction_id = self.kwargs.get('interaction_id')
        lead = get_object_or_404(Lead, id=lead_id)
        interaction = get_object_or_404(Interaction, id=interaction_id)
        form.instance.lead = lead
        form.instance.interaction = interaction
        messages.success(self.request, "Note added successfully!")
        return super().form_valid(form)

# Document Upload View
class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'interaction/document_form.html'

    def form_valid(self, form):
        lead_id = self.kwargs.get('lead_id')
        interaction_id = self.kwargs.get('interaction_id')
        lead = get_object_or_404(Lead, id=lead_id)
        form.instance.lead = lead
        form.instance.uploaded_by = self.request.user
        if interaction_id:
            interaction = get_object_or_404(Interaction, id=interaction_id)
            form.instance.interaction = interaction
        messages.success(self.request, "Document uploaded successfully!")
        return super().form_valid(form)


def autocomplete_lead_name(request):
    query = request.GET.get('lead_name', '')
    leads = Lead.objects.filter(name__icontains=query)
    results = [{'id': lead.id, 'name': lead.name} for lead in leads]
    return JsonResponse({'data': results})

def autocomplete_details(request):
    query = request.GET.get('details', '')
    interactions = Interaction.objects.filter(details__icontains=query)
    results = [{'id': interaction.id, 'details': interaction.details} for interaction in interactions]
    return JsonResponse({'data': results})
