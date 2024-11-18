from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Reservation

def customer_menu(request):
    return render(request, 'customer/customer_menu.html')

@login_required
def manage_reservations(request):
    reservations = Reservation.objects.filter(cust=request.user)
    return render(request, 'customer/manage_reservations.html', {'reservations': reservations})