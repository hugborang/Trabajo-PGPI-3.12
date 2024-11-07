# models/user.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    surnames = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('propietario', 'Propietario'),
        ('inquilino', 'Inquilino'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='inquilino')

    # Especificar un related_name único para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Cambia esto a un nombre único
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Cambia esto a un nombre único
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username


 # Métodos adicionales para verificar el rol
    @property
    def is_propietario(self):
        return self.role == 'propietario'

    @property
    def is_inquilino(self):
        return self.role == 'inquilino'