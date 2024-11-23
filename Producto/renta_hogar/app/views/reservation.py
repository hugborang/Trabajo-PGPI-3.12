from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from app.models import Apartment, Reservation
from app.forms.reservation_form import ReservationForm
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime
from app.models import Apartment, Reservation
from app.utils.decorator import requires_role
import json


@login_required
@requires_role("customer")
def create_reservation(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    current_year = datetime.now().year
    
    reservations = Reservation.objects.filter(apartment=apartment)
    reserved_days = []

    for reservation in reservations:
        reserved_days += reservation.reserved_days()  

    reserved_dates = [reserved_day.strftime('%Y-%m-%d') for reserved_day in reserved_days]

    reserved_dates_json = json.dumps(reserved_dates)

    days = range(1, 32)
    months = [{"value": i, "name": datetime(2000, i, 1).strftime("%B")} for i in range(1, 13)]
    years = list(range(current_year, current_year + 5))

    errors = []

    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        reservation = Reservation(
            cust=request.user,
            apartment=apartment,
            start_date=start_date,
            end_date=end_date,
            total_price=apartment.price * (end_date - start_date).days
        )
        reservation.full_clean()  
        reservation.save()

        return redirect("manage_reservations")  

    return render(request, "customer/create_reservation.html", {
        "apartment": apartment,
        "days": days,
        "months": months,
        "years": years,
        "errors": errors,
        "reserved_dates": reserved_dates_json,  # Pasar las fechas en formato JSON
    })


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if reservation.cust != request.user:
        return HttpResponseForbidden("No tienes permiso para cancelar esta reserva.")

    # No permitir cancelar la reserva un día antes de la fecha de inicio
    if (reservation.start_date - timezone.now().date()).days <= 1:
        return HttpResponseForbidden("No se puede cancelar una reserva un día antes de su fecha de inicio.")

    if request.method == "POST":
        reservation.delete()
        return redirect("manage_reservations")

    return render(request, "reservation/confirm_delete.html", {"reservation": reservation})