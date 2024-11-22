from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def manage_availability(request, apartment_id):
    # Verificar que el usuario sea un propietario
    if request.user.role != 'owner':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')
    
    # Verificar que el apartamento exista
    apartment = get_object_or_404(Apartment, id=apartment_id)

    # Verificar que el apartamento pertenezca al propietario
    if apartment.owner != request.user:
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    availabilities = apartment.availabilities.all()
    return render(request, 'owner/manage_availability.html', {'apartment': apartment, 'availabilities': availabilities})

