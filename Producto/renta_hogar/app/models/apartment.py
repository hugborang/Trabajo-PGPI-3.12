from django.db import models
from django.conf import settings

class Apartment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apartments",
        limit_choices_to={'role': 'owner'}
    )
    address = models.CharField(max_length=255)
    #photos = models.ImageField(upload_to="apartments/photos", blank=True, null=True)
    guest_count = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)

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
