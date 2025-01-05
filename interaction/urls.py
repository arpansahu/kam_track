from django.urls import path
from .views import (
    InteractionListView, InteractionCreateView, InteractionDetailView, InteractionUpdateView,
    TaskListView, TaskCreateView, NoteCreateView, DocumentCreateView,

    autocomplete_lead_name, autocomplete_details
)

urlpatterns = [
    path('interactions/', InteractionListView.as_view(), name='interaction-list'),
    path('interactions/add/<uuid:lead_id>/', InteractionCreateView.as_view(), name='interaction-add'),
    path('interactions/<uuid:pk>/', InteractionDetailView.as_view(), name='interaction-detail'),
    path('interactions/<uuid:pk>/update/', InteractionUpdateView.as_view(), name='interaction-update'),

    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/add/<uuid:lead_id>/', TaskCreateView.as_view(), name='task-add'),

    path('notes/add/<uuid:lead_id>/<uuid:interaction_id>/', NoteCreateView.as_view(), name='note-add'),
    path('documents/add/<uuid:lead_id>/<uuid:interaction_id>/', DocumentCreateView.as_view(), name='document-add'),

    path('autocomplete/lead-name/', autocomplete_lead_name, name='autocomplete-lead-name'),
    path('autocomplete/details/', autocomplete_details, name='autocomplete-details'),
]
