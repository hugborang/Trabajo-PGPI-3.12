# views.py

from django.shortcuts import render
from app.models import Apartment


def search_apartment(request):
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    huespedes = request.GET.get('huespedes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    apartments = Apartment.objects.filter(is_visible=True) 

    if price_min:
        apartments = apartments.filter(price__gte=price_min, is_visible=True)
    if price_max:
        apartments = apartments.filter(price__lte=price_max, is_visible=True)
    if huespedes:
        apartments = apartments.filter(guest_count=huespedes, is_visible=True)
    if fecha_inicio and fecha_fin:
        apartments = apartments.exclude(
            availabilities__start_date__lt=fecha_fin,
            availabilities__end_date__gt=fecha_inicio
        ).filter(is_visible=True)


    return render(request, 'home.html', {
        'apartments': apartments,
        'request': request  
    })
