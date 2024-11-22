from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion_correo(asunto, mensaje, destinatario):
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,  # Dirección desde la que se envía
        [destinatario],            # Lista de destinatarios
        fail_silently=False,       # Cambia a True si no quieres que Django lance errores
    )


from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Reservation

@receiver(post_save, sender=Reservation)
def notificar_evento_especial(sender, instance, created, **kwargs):
    if created:  # Si la reserva es nueva
        asunto = "Nueva reserva creada"
        mensaje = f"Se ha creado una nueva reserva para el piso {instance.apartment.address}."
        destinatario = "tu_correo@gmail.com"
        enviar_notificacion_correo(asunto, mensaje, destinatario)
