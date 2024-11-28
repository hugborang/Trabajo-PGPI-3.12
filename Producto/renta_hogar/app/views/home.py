from django.shortcuts import render
from django.db.models import Q
from app.models import Apartment
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError


def search_apartment(request):
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    huespedes = request.GET.get('huespedes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    apartments = Apartment.objects.filter(is_visible=True)
    error_message = None

    if huespedes:
        try:
            huespedes = int(huespedes)
            if huespedes < 1:
                error_message = "El número de huéspedes debe ser mayor a 0."
            else:
                apartments = apartments.filter(guest_count=huespedes)
        except ValueError:
            error_message = "El número de huéspedes debe ser un número entero."

    if price_min:
        try:
            price_min = float(price_min)
            apartments = apartments.filter(price__gte=price_min)
        except ValueError:
            error_message = "El precio mínimo debe ser un número válido."

    if price_max:
        try:
            price_max = float(price_max)
            apartments = apartments.filter(price__lte=price_max)
        except ValueError:
            error_message = "El precio máximo debe ser un número válido."

    if price_min and price_max and price_max < price_min:
        error_message = "El precio máximo no puede ser menor al precio mínimo."

    if fecha_inicio and fecha_fin:           
        try:
            start_date = parse_date(fecha_inicio)
            end_date = parse_date(fecha_fin)

            apartments = apartments.filter(
                Q(availabilities__start_date__lte=start_date) &
                Q(availabilities__end_date__gte=end_date)
            )
        except ValueError:  # Si las fechas no son válidas, lanzamos un mensaje
            error_message = "Las fechas deben ser válidas."

    return render(request, 'home.html', {
        'apartments': apartments.distinct(),
        'request': request,
        'error_message': error_message,
    })
