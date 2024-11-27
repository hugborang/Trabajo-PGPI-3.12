from django.db import models
from django.conf import settings
from .apartment import Apartment

class Review(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField(blank=True)  # Comentario opcional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.apartment}"
