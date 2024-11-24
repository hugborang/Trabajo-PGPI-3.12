from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Apartment
from app.models.review import Review
from app.utils.decorator import requires_role  

@login_required
@requires_role('owner')
def owner_menu(request):
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

@login_required
def owner_reviews(request):
    
    if request.user.role != 'owner':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('home')

    apartments = Apartment.objects.filter(owner=request.user) 

    # Obtener las valoraciones de cada apartamento
    reviews = {}
    for apartment in apartments:
        reviews[apartment] = Review.objects.filter(apartment=apartment)

    return render(request, 'owner/review_list.html', {'reviews': reviews})