from django.contrib import admin
from .models.user import CustomUser  # Asegúrate de importar el modelo correcto
from .models.apartment import Apartment
from .models.availability import Availability
from .models.apartmentPhoto import ApartmentPhoto

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')  # Añade los campos que quieras mostrar
    search_fields = ('username', 'email')  # Campos que se pueden buscar en el admin
    list_filter = ('role', 'is_staff', 'is_active')  # Filtros disponibles en el admin

class ApartmentPhotoInline(admin.TabularInline):
    model = ApartmentPhoto
    extra = 1
    
@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('address', 'owner', 'guest_count', 'is_visible')
    search_fields = ('address', 'owner__username')
    list_filter = ('is_visible', 'guest_count')
    inlines = [ApartmentPhotoInline]  # Permite agregar fotos al editar un apartamento

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'start_date', 'end_date')
    search_fields = ('apartment__address',)
    list_filter = ('start_date', 'end_date')

@admin.register(ApartmentPhoto)
class ApartmentPhotoAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'uploaded_at')
    search_fields = ('apartment__address',)