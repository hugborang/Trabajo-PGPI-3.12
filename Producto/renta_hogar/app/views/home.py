from django.shortcuts import render
from django.db.models import Q
from app.models import Apartment
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.utils.timezone import now


def search_apartment(request):
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    huespedes = request.GET.get('huespedes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    apartments = Apartment.objects.filter(is_visible=True)
    error_messages = []

    if huespedes:
        try:
            huespedes = int(huespedes)
            if huespedes < 1:
                error_messages.append("El número de huéspedes debe ser mayor a 0.")
            else:
                apartments = apartments.filter(guest_count=huespedes)
        except ValueError:
            error_messages.append("El número de huéspedes debe ser un número entero.")

    if price_min:
        try:
            price_min = float(price_min)
            if price_min >0:
                apartments = apartments.filter(price__gte=price_min)
            else:
                error_messages.append("El precio mínimo debe ser mayor a 0.")
        except ValueError:
            error_messages.append("El precio mínimo debe ser un número válido.")

    if price_max:
        try:
            price_max = float(price_max)
            if price_max > 0:
                apartments = apartments.filter(price__lte=price_max)
            else:
                error_messages.append("El precio máximo debe ser mayor a 0.")
        except ValueError:
            error_messages.append("El precio máximo debe ser un número válido.")

    if price_min and price_max and price_max < price_min:
        error_messages.append("El precio máximo no puede ser menor al precio mínimo.")

    if fecha_inicio and fecha_fin:           
        try:
            start_date = parse_date(fecha_inicio)
            end_date = parse_date(fecha_fin)

            if start_date < now().date() or end_date < now().date():
                error_messages.append("Las fechas no pueden ser anteriores a la fecha actual.")
            elif start_date > end_date:
                error_messages.append("La fecha de entrada no puede ser posterior a la fecha de salida.")    
            else:
                apartments = apartments.filter(
                    Q(availabilities__start_date__lte=start_date) &
                    Q(availabilities__end_date__gte=end_date)
                )
        except ValueError:
            error_messages.append("Las fechas deben ser válidas.")

    if error_messages:
        apartments = Apartment.objects.none()

    return render(request, 'home.html', {
        'apartments': apartments.distinct(),
        'request': request,
        'error_messages': error_messages,
    })
