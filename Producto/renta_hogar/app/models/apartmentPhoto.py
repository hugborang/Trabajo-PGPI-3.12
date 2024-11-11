# models/apartment_photo.py
from django.db import models
from django.core.exceptions import ValidationError
from .apartment import Apartment
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        raise ValidationError("Solo se permiten archivos de imagen con las extensiones: .jpg, .jpeg, .png, .gif")

class ApartmentPhoto(models.Model):
    apartment = models.ForeignKey(
        Apartment, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    photo = models.ImageField(
        upload_to="apartments/photos",
        validators=[validate_image_extension],  # Valida solo imágenes con extensiones específicas
        verbose_name="Foto del apartamento"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.apartment.address}"
