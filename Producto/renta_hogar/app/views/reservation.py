from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from app.models import Apartment, Reservation
from app.forms.reservation_form import ReservationForm
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.db.models import F
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
    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        return render(request, '404.html', status=404)

    reservations = Reservation.objects.filter(apartment=apartment)
    reserved_days = []

    for reservation in reservations:
        reserved_days += reservation.reserved_days()

    reserved_dates = [reserved_day.strftime('%Y-%m-%d') for reserved_day in reserved_days]
    reserved_dates_json = json.dumps(reserved_dates)

    errors = []

    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        overlapping_reservations = Reservation.objects.filter(
            apartment=apartment,
            end_date__gt=start_date,
            start_date__lt=end_date
        )
        if overlapping_reservations.exists():
            errors.append("El apartamento no está disponible en las fechas seleccionadas.")

        if not errors:
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
                            'unit_amount': int(reservation.total_price * 100),  
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/verify_payment/') + "?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=request.build_absolute_uri('/reservation/' + str(apartment_id) + "/"),
                    metadata={  
                    'apartment_id': str(apartment.id),
                    'start_date': start_date.strftime("%Y-%m-%d"),
                    'end_date': end_date.strftime("%Y-%m-%d"),
                    },
                )

                reservation.session_id = session.id  
                reservation.status = 'pending'
                return redirect(session.url, code=303)  

            except Exception as e:
                errors.append(f"Error al crear la sesión de pago: {str(e)}")

    return render(request, "customer/create_reservation.html", {
        "apartment": apartment,
        "errors": errors,
        "reserved_dates": reserved_dates_json,
    })
    
    
@login_required
@requires_role("customer")
def verify_payment(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return render(request, "customer/payment_failed.html", {
            "error": "No se proporcionó un session_id.",
        })

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            if Reservation.objects.filter(
                cust=request.user,
                apartment=Apartment.objects.get(id=session.metadata['apartment_id']),
                start_date=datetime.strptime(session.metadata['start_date'], "%Y-%m-%d"),
                end_date=datetime.strptime(session.metadata['end_date'], "%Y-%m-%d"),
            ).exists():
                return render(request, "customer/payment_failed.html", {
                        "error": "Ya tienes una reserva para este apartamento en estas fechas.",
                        })
            
            reservation = Reservation(
                cust=request.user,
                apartment=Apartment.objects.get(id=session.metadata['apartment_id']),
                start_date=datetime.strptime(session.metadata['start_date'], "%Y-%m-%d"),
                end_date=datetime.strptime(session.metadata['end_date'], "%Y-%m-%d"),
                total_price=float(session.amount_total) / 100,
            )
            reservation.save()

            # Enviar notificaciones l customer
            enviar_notificacion_correo(
                f"¡FELICIDADES! Pago exitoso para la reserva de {reservation.apartment.address}",
                f"Has reservado del {reservation.start_date} al {reservation.end_date} en el apartamento situado en  {reservation.apartment.address} del propietario {reservation.apartment.owner.username}, contacta con el propietario mediante su email: {reservation.apartment.owner.email}. \nRecuerda que puedes cancelar la reserva hasta 30 días de la fecha de entrada . ¡Disfruta de tu estancia!",
                request.user.email
            )
            
            # Enviar notificaciones al propietario
            enviar_notificacion_correo(
                f"¡FELICIDADES! Pago exitoso para la reserva de {reservation.apartment.address}",
                f"Se ha reservado del {reservation.start_date} al {reservation.end_date} en el apartamento situado en {reservation.apartment.address} por el cliente {request.user.username}, su email de contacto es: {request.user.email}. \nRecuerda que el cliente puede cancelar la reserva hasta 30 días de la fecha de entrada.",
                reservation.apartment.owner.email
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



from django.shortcuts import render, redirect, get_object_or_404

@login_required
@requires_role("customer")
def delete_reservation(request, reservation_id):

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return render(request, '404.html', status=404)
    
    if reservation.cust != request.user:
        return render(request, 'access_denied.html', status=403)
    reservations = Reservation.objects.filter(cust=request.user)
    if reservation.cust != request.user:
        return HttpResponseForbidden("No tienes permiso para cancelar esta reserva.")
    

    if request.method == "POST":
        
        # Enviar notificación al cliente
        enviar_notificacion_correo(
            f"Reserva cancelada para el apartamento {reservation.apartment.address}",
            f"La reserva del apartamento {reservation.apartment.address} ha sido cancelada.\n"
            f"Si tienes alguna duda, contacta con el propietario {reservation.apartment.owner.username} mediante su email: {reservation.apartment.owner.email}.",
            request.user.email
        )
        
        # Enviar notificación al propietario
        enviar_notificacion_correo(
            f"Reserva cancelada para el apartamento {reservation.apartment.address}",
            f"La reserva del apartamento {reservation.apartment.address} ha sido cancelada por el cliente {request.user.username}.\n"
            f"Puedes contactar con el cliente mediante su email: {request.user.email}.",
            reservation.apartment.owner.email
        )
        reservation.delete()

        
        return redirect("manage_reservations")

    return render(request, 'customer/manage_reservations.html', {'reservations': reservations})



@login_required
@requires_role("owner")
def delete_reservation_owner(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return render(request, '404.html', status=404)

    if reservation.apartment.owner != request.user:
        return HttpResponseForbidden("No tienes permiso para cancelar esta reserva.")

    # Continúa con la lógica de cancelación si el propietario coincide
    reservations = Reservation.objects.filter(cust=request.user)
    if request.method == "POST":
        
        # Enviar notificación al cliente
        enviar_notificacion_correo(
            f"Reserva cancelada para el apartamento {reservation.apartment.address}",
            f"La reserva del apartamento {reservation.apartment.address} ha sido cancelada por el proppietario.\n"
            f"Si tienes alguna duda, contacta con el propietario {reservation.apartment.owner.username} mediante su email: {reservation.apartment.owner.email}.",
            request.user.email
        )
        
        # Enviar notificación al propietario
        enviar_notificacion_correo(
            f"Reserva cancelada para el apartamento {reservation.apartment.address}",
            f"La reserva del apartamento {reservation.apartment.address} ha sido cancelada {request.user.username}.\n"
            f"Puedes contactar con el cliente mediante su email: {request.user.email}.",
            reservation.apartment.owner.email
        )
        reservation.delete()

        return redirect("owner_reservations")

    return render(request, 'owner/manage_reservations.html', {'reservations': reservations})

