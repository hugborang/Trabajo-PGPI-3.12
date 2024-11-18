from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Apartment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apartments",
        limit_choices_to={'role': 'owner'}
    )
    address = models.CharField(max_length=255, unique=True)
    guest_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="La capacidad de huéspedes debe ser mayor que 0")],
    )
    description = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,
                                validators=[MinValueValidator(0, message="El precio no puede ser negativo")],
                                )


    def __str__(self):
        return f"{self.address} - {self.owner.username}"

    def delete(self, *args, **kwargs):
        if self.has_reservations():
            raise ValueError("No se puede eliminar un apartamento con reservas asociadas.")
        super().delete(*args, **kwargs)

    def has_reservations(self):
        return self.availabilities.exists()

    def is_available(self, start_date, end_date):
        overlapping_availabilities = self.availabilities.filter(
            start_date__lt=end_date, end_date__gt=start_date
        )
        return not overlapping_availabilities.exists()
