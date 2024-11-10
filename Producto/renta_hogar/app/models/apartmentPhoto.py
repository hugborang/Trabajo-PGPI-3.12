# models/apartment_photo.py
from django.db import models
from .apartment import Apartment

class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(
        Apartment, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    photo = models.ImageField(upload_to="apartments/photos")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.apartment.address}"
