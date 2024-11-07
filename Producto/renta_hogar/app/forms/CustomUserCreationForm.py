from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')  # Asegúrate de incluir el campo 'role'
