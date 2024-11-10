from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Apartment  # Importa el modelo Apartment

@login_required
def owner_menu(request):
    # Verificar que el usuario sea un propietario
    if request.user.role != 'owner':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')  # Redirige a la página principal si no es propietario

    # Obtener los apartamentos asociados al propietario
    apartments = Apartment.objects.filter(owner=request.user)
    return render(request, 'owner/owner_menu.html', {'apartments': apartments})
