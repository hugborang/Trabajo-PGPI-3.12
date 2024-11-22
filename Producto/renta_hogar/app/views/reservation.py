from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from app.models import Apartment, Reservation
from app.forms.reservation_form import ReservationForm
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from datetime import datetime

@login_required
def create_reservation(request, apartment_id):
    if request.user.role != "customer":
        return HttpResponseForbidden("Solo los inquilinos pueden realizar reservas.")

    apartment = get_object_or_404(Apartment, id=apartment_id)

    errors = []

    if request.method == "POST":
        start_date = datetime.strptime(request.POST["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.POST["end_date"], "%Y-%m-%d").date()
        for date in apartment.availabilities.all():
            if date.start_date <= start_date and date.end_date >= end_date:
                break
            errors.append("El apartamento no está disponible en las fechas seleccionadas.")
            return render(request, "customer/create_reservation.html", {
                "apartment": apartment,
                "errors": errors,
            })

        try:
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
        except ValidationError as e:
            errors.extend(e.messages)

    return render(request, "customer/create_reservation.html", {
        "apartment": apartment,
        "errors": errors,
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
