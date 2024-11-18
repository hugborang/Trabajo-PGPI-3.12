from django.db import models
from django.conf import settings
from app.models import Apartment
from django.core.exceptions import ValidationError
from django.utils import timezone

class Reservation(models.Model):
    cust = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="reservations"
    )
    apartment = models.ForeignKey(
        Apartment, 
        on_delete=models.CASCADE, 
        related_name="reservations"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        # Validación de fechas futuras
        if self.start_date < timezone.now().date():
            raise ValidationError("La fecha de inicio debe ser en el futuro.")
        if self.end_date < timezone.now().date():
            raise ValidationError("La fecha de fin debe ser en el futuro.")

        # Validación de rango de fechas
        if self.start_date >= self.end_date:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")

        # Validación de solapamiento
        overlapping_reservations = Reservation.objects.filter(
            apartment=self.apartment,
            end_date__gt=self.start_date,
            start_date__lt=self.end_date
        ).exclude(id=self.id)
        if overlapping_reservations.exists():
            raise ValidationError("El apartamento no está disponible en las fechas seleccionadas.")

    def __str__(self):
        return f"Reserva de {self.cust.username} en {self.apartment.address} ({self.start_date} - {self.end_date})"

