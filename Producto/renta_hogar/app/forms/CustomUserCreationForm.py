from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from app.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')  # Asegúrate de incluir el campo 'role'
        
        
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email'] 
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        label='Nueva contraseña',
        required=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        label='Confirmar nueva contraseña',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if not password1:
                self.add_error('password1', "Debes ingresar una nueva contraseña.")
            if not password2:
                self.add_error('password2', "Debes confirmar la nueva contraseña.")
            if password1 != password2:
                self.add_error('password2', "Las contraseñas no coinciden.")

            try:
                validate_password(password1)  
            except ValidationError as e:
                self.add_error('password1', e.messages)
        return cleaned_data