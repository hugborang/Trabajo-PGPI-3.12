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
def owner_reviews(request):
    if request.user.role != 'owner':
        return render(request, 'access_denied.html', status=403)

    apartments = Apartment.objects.filter(owner=request.user) 

    if apartments.exists():
        reviews = {}
        for apartment in apartments:
            reviews[apartment] = Review.objects.filter(apartment=apartment)
    
    return render(request, 'owner/review_list.html', {'reviews': reviews})