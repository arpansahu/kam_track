from django import forms
from django.utils.timezone import now

class CustomInteractionForm(forms.Form):
    contact = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}))
    interaction_type = forms.ChoiceField(
        choices=[('call', 'Call'), ('meeting', 'Meeting'), ('order', 'Order')],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'interaction-type'}),
    )
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    interaction_date = forms.DateTimeField(
        initial=now,  # Set default to current timezone-aware datetime
        widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
    )
    duration_minutes = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    order_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    currency = forms.ChoiceField(
        choices=[('USD', 'US Dollars'), ('EUR', 'Euros'), ('INR', 'Indian Rupees'), ('GBP', 'British Pounds'), ('AUD', 'Australian Dollars')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='USD',  # Default currency set to USD
        required=False,
    )

    def __init__(self, *args, **kwargs):
        contacts_queryset = kwargs.pop('contacts_queryset', None)
        interaction_type_initial = kwargs.pop('interaction_type_initial', None)
        super().__init__(*args, **kwargs)

        if interaction_type_initial:
            self.fields['interaction_type'].widget.attrs['readonly'] = True
            self.initial['interaction_type'] = interaction_type_initial

        if contacts_queryset:
            self.fields['contact'].choices = [(contact.id, contact.name) for contact in contacts_queryset]

    def clean_interaction_date(self):
        interaction_date = self.cleaned_data.get('interaction_date')
        if interaction_date and interaction_date < now():
            raise forms.ValidationError("You cannot set a time that has already passed.")
        return interaction_date

    def clean(self):
        cleaned_data = super().clean()
        interaction_type = cleaned_data.get('interaction_type')
        order_amount = cleaned_data.get('order_amount')
        currency = cleaned_data.get('currency')

        if interaction_type == 'order':
            if not order_amount:
                self.add_error('order_amount', "Order amount is required for order interactions.")
            if not currency:
                self.add_error('currency', "Currency is required for order interactions.")
        return cleaned_data
