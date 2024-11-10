from django.contrib import admin
from .models.user import CustomUser  # Asegúrate de importar el modelo correcto

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')  # Añade los campos que quieras mostrar
    search_fields = ('username', 'email')  # Campos que se pueden buscar en el admin
    list_filter = ('role', 'is_staff', 'is_active')  # Filtros disponibles en el admin
