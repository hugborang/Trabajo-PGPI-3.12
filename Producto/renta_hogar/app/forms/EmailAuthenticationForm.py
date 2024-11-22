from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django import forms
from app.models import CustomUser


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=254)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

       

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.check_password(password):
                    self.add_error('password', 'Contraseña incorrecta.')
                self.user = user
            except CustomUser.DoesNotExist:
                self.add_error('email', 'Correo electrónico incorrecto.')
        return self.cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)  