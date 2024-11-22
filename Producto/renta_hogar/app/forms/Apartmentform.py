# forms.py
from django import forms
from app.models import Apartment

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['address', 'guest_count', 'description', 'is_visible', 'price']
        labels = {
            'address': 'Dirección',
            'guest_count': 'Cantidad de huéspedes',
            'description': 'Descripción',
            'is_visible': '¿Disponible?',
            'price': 'Precio',
        }
