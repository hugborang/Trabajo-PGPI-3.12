from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion_correo(asunto, mensaje, destinatario):
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,  
        [destinatario],            
        fail_silently=False,      
    )
