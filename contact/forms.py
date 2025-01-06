from django import forms
from .models import Contact
from lead.models import Lead  # Import Lead model

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'role', 'email', 'country_code', 'phone_number', 'lead']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter role or designation'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'country_code': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'lead': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Lead'}),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)  # Pop user to filter leads by KAM
        super().__init__(*args, **kwargs)
        if self.request_user:
            self.fields['lead'].queryset = Lead.objects.filter(assigned_kam=self.request_user)
        else:
            self.fields['lead'].queryset = Lead.objects.none()  # Empty queryset if no user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        contact_id = self.instance.pk  # Get the current contact's ID during update
        if email and Contact.objects.filter(email=email).exclude(pk=contact_id).exists():
            raise forms.ValidationError("A contact with this email address already exists.")
        return email

    def clean_lead(self):
        lead = self.cleaned_data.get('lead')
        if not lead:
            raise forms.ValidationError("Please select a valid lead.")
        return lead
