from django import forms
from app.models.review import Review
from django.core.exceptions import ValidationError
from django.utils import timezone
from app.models import Reservation

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control',
                'placeholder': 'Ingresa una valoración (1-5)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deja un comentario (opcional)',
                'rows': 4
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  
        self.apartment = kwargs.pop('apartment', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        comment = cleaned_data.get('comment')

        if not self.request:
            raise ValidationError("Se requiere un objeto request.")

        reservation = Reservation.objects.get(cust=self.request.user, apartment=self.apartment)  
        if reservation.end_date > timezone.now().date():
            raise ValidationError("La reserva debe haber finalizado para dejar una valoración.")

        if Review.objects.filter(user=self.request.user, apartment=self.apartment).exists():
            raise ValidationError("Ya has dejado una valoración para este apartamento.")

        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)
