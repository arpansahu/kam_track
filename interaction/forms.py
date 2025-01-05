from django import forms
from .models import Interaction, Task, Note, Document

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'details', 'interaction_date', 'duration_minutes', 'order_amount']
        widgets = {
            'interaction_type': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'interaction_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_type', 'due_date', 'completed']
        widgets = {
            'task_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control datetimepicker'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
