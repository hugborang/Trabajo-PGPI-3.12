# forms/reservation_form.py
from django import forms
from app.models.reservation import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']
