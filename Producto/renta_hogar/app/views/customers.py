from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render
from app.models import reservation
from app.models import Apartment    
from django.contrib.auth.decorators import login_required
from app.models import Reservation
from app.utils.decorator import requires_role
from django.utils.dateparse import parse_date

@login_required
@requires_role('customer')
def customer_menu(request):
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    huespedes = request.GET.get('huespedes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    apartments = Apartment.objects.filter(is_visible=True)  # Filtrar solo apartamentos visibles

    if price_min:
        price_min = float(price_min)
        apartments = apartments.filter(price__gte=price_min, is_visible=True)
    if price_max:
        price_max = float(price_max)
        apartments = apartments.filter(price__lte=price_max, is_visible=True)
    if huespedes:
        huespedes = int(huespedes)
        apartments = apartments.filter(guest_count=huespedes, is_visible=True)
    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        apartments = apartments.filter(
        availabilities__start_date__lte=fecha_inicio,
        availabilities__end_date__gte=fecha_fin,
        is_visible=True
        )

    return render(request, 'customer/customer_menu.html', {
        'apartments': apartments.distinct(),
        'request': request  
    })

@login_required
@requires_role('customer')
def manage_reservations(request):
    reservations = Reservation.objects.filter(cust=request.user)
    
    now = datetime.now().date()
    
    for r in reservations:
        if r.start_date - now < timedelta(days=30):
            r.can_cancel = False
            r.save()
            
    return render(request, 'customer/manage_reservations.html', {'reservations': reservations, 'now': now})
