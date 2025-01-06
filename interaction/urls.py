from django.urls import path
from .views import (
    InteractionListView, InteractionCreateView, InteractionDetailView, InteractionUpdateView,

)

urlpatterns = [
    path('', InteractionListView.as_view(), name='interaction-list'),
    path('add/', InteractionCreateView.as_view(), name='interaction-add'),
    path('<uuid:pk>/', InteractionDetailView.as_view(), name='interaction-detail'),
    path('<uuid:pk>/update/', InteractionUpdateView.as_view(), name='interaction-update'),
]
