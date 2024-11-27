from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Apartment
from app.models.review import Review
from app.utils.decorator import requires_role  
from app.models import Reservation

@login_required
@requires_role('owner')
def owner_menu(request):
    apartments = Apartment.objects.filter(owner=request.user)
    return render(request, 'owner/owner_menu.html', {'apartments': apartments})

@login_required
@requires_role('owner')
def manage_availability(request, apartment_id):
    # Verificar que el usuario sea un propietario
    if request.user.role != 'owner':
        return render(request, 'access_denied.html', status=403)
    
    # Verificar que el apartamento exista
    try:
        apartment = Apartment.objects.get(id=apartment_id)

        if apartment.owner != request.user:
            return render(request, 'access_denied.html', status=403)
        
        availabilities = apartment.availabilities.all()
        return render(request, 'owner/manage_availability.html', {'apartment': apartment, 'availabilities': availabilities})
    except Apartment.DoesNotExist:
        return render(request, '404.html', status=404)

@login_required
@requires_role('owner')
def owner_reviews(request):
    
    apartments = Apartment.objects.filter(owner=request.user) 

    # Obtener las valoraciones de cada apartamento
    reviews = {}
    for apartment in apartments:
        reviews[apartment] = Review.objects.filter(apartment=apartment)

    return render(request, 'owner/review_list.html', {'reviews': reviews})


@login_required
@requires_role('owner')
def owner_reservations(request):
    # Obtener los apartamentos del propietario autenticado
    owner_apartments = Apartment.objects.filter(owner=request.user)
    
    # Filtrar las reservas relacionadas con estos apartamentos
    reservations = Reservation.objects.filter(apartment__in=owner_apartments)
    
    return render(request, 'owner/manage_reservations.html', {'reservations': reservations})
