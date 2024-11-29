from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden, Http404
from django.utils.timezone import now
from app.forms.Apartmentform import ApartmentForm
from app.forms.availability_form import AvailabilityForm
from app.models import Apartment, ApartmentPhoto, Availability, Reservation
from app.models.apartmentPhoto import validate_image_extension
from app.models.availability import validate_date_range
from django.shortcuts import redirect, get_object_or_404
from app.utils.decorator import requires_role

@login_required
@requires_role('owner')
def add_apartment(request):
    
    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        photo = request.FILES.get('photos')
        photo_errors = []

        if not photo:
            photo_errors.append("Debes subir al menos una foto del apartamento.")
        else:
            try:
                validate_image_extension(photo)
            except ValidationError as e:
                photo_errors.append(e.message)

        for error in photo_errors:
            form.add_error(None, error)

        if form.is_valid() and not photo_errors:
            apartment = form.save(commit=False)
            apartment.owner = request.user
            apartment.save()

            ApartmentPhoto.objects.create(apartment=apartment, photo=photo)
   
            return redirect('owner_menu')
        

        return render(request, 'owner/apartment_form.html', {'form': form, 'edit_mode': False, 'photo_errors': photo_errors})
    
    
    form = ApartmentForm()
    return render(request, 'owner/apartment_form.html', {'form': form, 'edit_mode': False, 'photo_errors': []})



@login_required
@requires_role('owner')
def delete_apartment(request, apartment_id):
    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        return render(request, '404.html', status=404)

    if request.method == "POST":
        # Verificar si el usuario es el propietario del apartamento
        if apartment.owner != request.user:
            return render(request, 'access_denied.html', status=403)
        
        # Verificar si existen reservas asociadas al apartamento
        if Reservation.objects.filter(apartment=apartment).exists():
            messages.error(request, "Este apartamento no puede ser eliminado porque tiene reservas asociadas.", extra_tags="delete_apartment")
            return redirect('owner_menu')

        apartment.delete()
        return redirect('owner_menu')

    return redirect('owner_menu')



@login_required
@requires_role('owner')
def edit_apartment(request, apartment_id):

    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        return render(request, '404.html', status=404)

    if apartment.owner != request.user:
        return render(request, 'access_denied.html', status=403)

    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        new_photo = request.FILES.get('photos')
        photo_errors = []

        if not new_photo and not apartment.photos.exists():
            photo_errors.append("El apartamento debe tener al menos una foto.")
        elif new_photo:
            try:
                validate_image_extension(new_photo)
            except ValidationError as e:
                photo_errors.append(e.message)

        for error in photo_errors:
            form.add_error(None, error)

        if form.is_valid() and not photo_errors:
            apartment = form.save(commit=False)
            apartment.owner = request.user
            apartment.save()

            # Elimina la foto existente
            if new_photo:
                apartment.photos.all().delete()
                ApartmentPhoto.objects.create(apartment=apartment, photo=new_photo)

            messages.success(request, "Apartamento editado exitosamente.")
            return redirect('owner_menu')

        return render(request, 'owner/apartment_form.html', {
            'form': form,
            'apartment': apartment,
            'edit_mode': True,
            'photo_errors': photo_errors
        })

    form = ApartmentForm(instance=apartment)
    return render(request, 'owner/apartment_form.html', {
        'form': form,
        'apartment': apartment,
        'edit_mode': True,
    })

@login_required
@requires_role('owner')
def add_availability(request, apartment_id):
    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        return render(request, '404.html', status=404)

    if apartment.owner != request.user:
        return render(request, 'access_denied.html', status=403)
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Validar que no se puede añadir disponibilidad en el pasado a partir de hoy
            if start_date < now().date() or end_date < now().date():
                form.add_error(None, "No puedes añadir disponibilidad en el pasado.")

            if not validate_date_range(apartment, start_date, end_date):
                form.add_error(None, "Ya existe una disponibilidad en ese rango de fechas para este apartamento.")

            if not form.errors:  # Si no hay errores, guardar
                Availability.objects.create(
                    apartment=apartment,
                    start_date=start_date,
                    end_date=end_date
                )
                return redirect('manage_availability', apartment_id=apartment_id)
            
        # Si el formulario tiene errores, renderizamos de nuevo
        return render(request, 'owner/add_availability.html', {
            'apartment': apartment,
            'form': form,
        })

    # En caso de GET, renderizar un formulario vacío
    form = AvailabilityForm()
    return render(request, 'owner/add_availability.html', {
        'apartment': apartment,
        'form': form,
    })


@login_required
@requires_role('owner')
def delete_availability(request, availability_id):

    try:
        availability = Availability.objects.get(id=availability_id)
        apartment_id = availability.apartment.id
        apartment = Apartment.objects.get(id=apartment_id)
    except Availability.DoesNotExist:
        return render(request, '404.html', status=404)

    if apartment.owner != request.user:
        return render(request, 'access_denied.html', status=403)
    
    if Reservation.objects.filter(apartment=apartment, start_date__gte=availability.start_date, end_date__lte=availability.end_date).exists():
        messages.error(request, "No puedes eliminar esta disponibilidad porque tiene reservas asociadas.", extra_tags="delete_availability")
        return redirect('manage_availability', apartment_id=apartment_id)

    if request.method == 'POST':
        availability.delete()
    return redirect('manage_availability', apartment_id=apartment_id)