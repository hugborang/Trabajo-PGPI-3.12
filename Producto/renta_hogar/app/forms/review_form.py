from django import forms
from app.models.review import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Campos que el usuario podrá llenar
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
