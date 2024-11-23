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
import stripe
from app.utils.correo import enviar_notificacion_correo

stripe.api_key = settings.STRIPE_SECRET_KEY
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

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Reserva de apartamento {apartment.address}',
                        },
                        'unit_amount': int(reservation.total_price * 100),  # Stripe trabaja con centavos
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/verify_payment/') + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri('/reservation/' + str(apartment_id) + "/"),
                metadata={  # Agrega los datos necesarios aquí
                'apartment_id': str(apartment.id),
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                },
            )

            # Guardamos la reserva antes de redirigir, pero no la confirmamos hasta que el pago se complete.
            reservation.session_id = session.id  # Guarda el session_id para referencia posterior
            reservation.status = 'pending'  # Estado pendiente, no confirmado aún

            return redirect(session.url, code=303)  # Redirige a Stripe para completar el pago

        except Exception as e:
            errors.append(f"Error al crear la sesión de pago: {str(e)}")

    return render(request, "customer/create_reservation.html", {
        "apartment": apartment,
        "days": days,
        "months": months,
        "years": years,
        "errors": errors,
        "reserved_dates": reserved_dates_json,
    })
    
    
@login_required
def verify_payment(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return render(request, "customer/payment_failed.html", {
            "error": "No se proporcionó un session_id.",
        })

    try:
        # Verifica el estado del pago en Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            # Solo guarda la reserva si el pago fue exitoso
            reservation = Reservation(
                cust=request.user,
                apartment=Apartment.objects.get(id=session.metadata['apartment_id']),
                start_date=datetime.strptime(session.metadata['start_date'], "%Y-%m-%d"),
                end_date=datetime.strptime(session.metadata['end_date'], "%Y-%m-%d"),
                total_price=float(session.amount_total) / 100,
                session_id=session_id,  # Guarda el session_id para referencia futura
            )
            reservation.save()

            # Enviar notificaciones
            enviar_notificacion_correo(
                f"¡FELICIDADES! Pago exitoso para la reserva de {reservation.apartment.address}",
                f"Has reservado del {reservation.start_date} al {reservation.end_date}. ¡Disfruta de tu estancia!",
                request.user.email,
            )

            return render(request, "customer/payment_success.html", {
                "reservation": reservation,
            })
        else:
            return render(request, "customer/payment_failed.html", {
                "error": "El pago no fue exitoso.",
            })

    except stripe.error.StripeError as e:
        return render(request, "customer/payment_failed.html", {
            "error": f"Error de Stripe: {str(e)}",
        })
    except Exception as e:
        return render(request, "customer/payment_failed.html", {
            "error": f"Error desconocido: {str(e)}",
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