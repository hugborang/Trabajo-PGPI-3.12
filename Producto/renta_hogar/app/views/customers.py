from django.shortcuts import render
from app.models import Apartment    
from django.contrib.auth.decorators import login_required
from app.models import Reservation

def customer_menu(request):
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    huespedes = request.GET.get('huespedes')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    apartments = Apartment.objects.all()

    if price_min:
        apartments = apartments.filter(price__gte=price_min)
    if price_max:
        apartments = apartments.filter(price__lte=price_max)
    if huespedes:
        apartments = apartments.filter(guest_count=huespedes)
    if fecha_inicio and fecha_fin:
        apartments = apartments.exclude(
            availabilities__start_date__lt=fecha_fin,
            availabilities__end_date__gt=fecha_inicio
        )


    return render(request, 'customer/customer_menu.html', {
        'apartments': apartments,
        'request': request  
    })

@login_required
def manage_reservations(request):
    reservations = Reservation.objects.filter(cust=request.user)
    return render(request, 'customer/manage_reservations.html', {'reservations': reservations})