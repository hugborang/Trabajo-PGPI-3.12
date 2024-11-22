from django.db import models
from .apartment import Apartment

def validate_date_range(apartment, start_date, end_date):
    # Buscar solapamientos con las fechas existentes
    overlapping = Availability.objects.filter(
        apartment=apartment,
        start_date__lt=end_date,  # El rango existente comienza antes de que termine el nuevo rango
        end_date__gt=start_date   # El rango existente termina después de que empiece el nuevo rango
    )
    if overlapping.exists():
        return False
    return True


class Availability(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.apartment.address} ({self.start_date} to {self.end_date})"
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lt=models.F('end_date')),
                name="start_date_before_end_date",
                violation_error_message="La fecha de inicio debe ser anterior a la fecha de fin."
            )
        ]
