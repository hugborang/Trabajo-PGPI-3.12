import re
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django import forms

class CustomUser(AbstractUser):
    surnames = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('owner', 'Propietario'),
        ('customer', 'Inquilino'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set', 
        blank=True,
        help_text='Specific permissions for this user.'
    )


    def __str__(self):
        return f"{self.username}"
    
    
    @property
    def is_owner(self):
        return self.role == 'owner'

    @property
    def is_customer(self):
        return self.role == 'customer'