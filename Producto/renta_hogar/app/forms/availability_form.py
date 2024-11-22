# forms/reservation_form.py
from django import forms
from app.models.availability import Availability

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_date', 'end_date']