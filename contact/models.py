from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from kam_track.models import AbstractBaseModel
import phonenumbers


class Contact(AbstractBaseModel):
    COUNTRY_CODE_CHOICES = [
        ('+1', 'United States (+1)'),
        ('+44', 'United Kingdom (+44)'),
        ('+91', 'India (+91)'),
        ('+61', 'Australia (+61)'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator(message=_("Please enter a valid email address."))]
    )
    country_code = models.CharField(max_length=5, choices=COUNTRY_CODE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    contact_owner = models.ForeignKey(
        'account.Account',
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    lead = models.ForeignKey(
        'lead.Lead',  # String reference to avoid circular import
        on_delete=models.CASCADE,
        related_name='lead_contacts',
        null=True,
        blank=True
    )

    def clean_phone_number(self):
        if self.phone_number:
            full_number = f"{self.country_code}{self.phone_number}"
            try:
                parsed_number = phonenumbers.parse(full_number)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError(_("The phone number is not valid for the selected country code."))
            except phonenumbers.NumberParseException:
                raise ValidationError(_("Invalid phone number format."))

    def clean(self):
        if self.phone_number and not self.country_code:
            raise ValidationError(_("Country code is required when entering a phone number."))
        self.clean_phone_number()
        super().clean()

    def __str__(self):
        return f"{self.name} - {self.role} ({self.country_code} {self.phone_number})"
