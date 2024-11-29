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
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Nueva contraseña',
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar nueva contraseña',
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Las contraseñas no coinciden.") 

            try:
                validate_password(password1)  
            except ValidationError as e:
                self.add_error('password1', e.messages)
        return cleaned_data