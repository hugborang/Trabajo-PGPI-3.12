from django.db import models
from .apartment import Apartment

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
                name="start_date_before_end_date"
            ),
            models.UniqueConstraint(
                fields=['apartment', 'start_date', 'end_date'],
                name="unique_availability_range"
            )
        ]
