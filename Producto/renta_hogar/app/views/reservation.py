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

@login_required
def create_reservation(request, apartment_id):
    if request.user.role != "customer":
        return HttpResponseForbidden("Solo los inquilinos pueden realizar reservas.")

    apartment = get_object_or_404(Apartment, id=apartment_id)
    current_year = datetime.now().year

    # Rango para días, meses y años
    days = range(1, 32)
    months = [{"value": i, "name": datetime(2000, i, 1).strftime("%B")} for i in range(1, 13)]
    years = list(range(current_year, current_year + 5))

    errors = []

    if request.method == "POST":
        day_start = request.POST.get("start_day")
        month_start = request.POST.get("start_month")
        year_start = request.POST.get("start_year")
        day_end = request.POST.get("end_day")
        month_end = request.POST.get("end_month")
        year_end = request.POST.get("end_year")

        try:
            # Parsear las fechas
            start_date = datetime(year=int(year_start), month=int(month_start), day=int(day_start)).date()
            end_date = datetime(year=int(year_end), month=int(month_end), day=int(day_end)).date()

            # Crear y validar la reserva
            reservation = Reservation(
                cust=request.user,
                apartment=apartment,
                start_date=start_date,
                end_date=end_date,
                total_price=apartment.price * (end_date - start_date).days
            )
            reservation.full_clean()  # Valida con las reglas del modelo
            reservation.save()


            send_mail(
                "Nueva reserva creada",
                f"Se ha creado una nueva reserva para el piso en.",
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            return redirect("manage_reservations")  # Redirigir si todo está bien
        except ValidationError as e:
            errors.extend(e.messages)
        except (ValueError, TypeError):
            errors.append("Las fechas proporcionadas no son válidas.")

    return render(request, "customer/create_reservation.html", {
        "apartment": apartment,
        "days": days,
        "months": months,
        "years": years,
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