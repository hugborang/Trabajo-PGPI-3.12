# views.py

from django.shortcuts import render
from app.models import Apartment, CustomUser


def search_apartment(request):
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    huespedes = request.GET.get('huespedes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    apartments = Apartment.objects.filter(is_visible=True)
    error_message = None

    # Validar huespedes
    if huespedes:
        try:
            huespedes = int(huespedes)  # Convertir a entero
            apartments = apartments.filter(guest_count=huespedes, is_visible=True)
            if huespedes < 1:
                error_message = "El número de huéspedes debe ser mayor a 0."
        except ValueError:
            error_message = "El número de huéspedes debe ser un número entero."
    
    if price_max and price_max < price_min:
        error_message = "El precio máximo no puede ser menor al precio mínimo."

    # Validar precio mínimo
    if price_min:
        apartments = apartments.filter(price__gte=price_min, is_visible=True)
    
    # Validar precio máximo
    if price_max:
        apartments = apartments.filter(price__lte=price_max, is_visible=True)
    
    # Validar fechas
    if fecha_inicio and fecha_fin:
        apartments = apartments.exclude(
            availabilities__start_date__lt=fecha_fin,
            availabilities__end_date__gt=fecha_inicio
        ).filter(is_visible=True)

    return render(request, 'home.html', {
        'apartments': apartments,
        'request': request,
        'error_message': error_message
    })
