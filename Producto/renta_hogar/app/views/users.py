from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from app.forms.CustomUserCreationForm import CustomUserCreationForm  

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('/auth/login/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # Redireccionar según el rol del usuario
            if user.role == 'inquilino':
                return redirect('book/')  # Asegúrate de que 'book' esté definido en tus URLs
            elif user.role == 'propietario':
                return redirect('owner_dashboard')  # Cambia esto a la vista adecuada para propietarios
            
            return redirect('home')  # Redirige a una página predeterminada si no coincide ningún rol
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})