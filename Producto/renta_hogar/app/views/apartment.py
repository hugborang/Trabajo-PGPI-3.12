from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden, Http404
from app.forms.Apartmentform import ApartmentForm
from app.models import Apartment, ApartmentPhoto
from app.models.apartmentPhoto import validate_image_extension
from django.shortcuts import redirect
from app.utils.decorator import requires_role

@login_required
@requires_role('owner')
def add_apartment(request):
    if request.user.role != 'owner':
        return HttpResponseForbidden("No tienes permiso para añadir apartamentos.")

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        photos = request.FILES.getlist('photos')
        photo_errors = []

        if not photos:
            photo_errors.append("Debes subir al menos una foto del apartamento.")
        elif len(photos) > 5:
            photo_errors.append("Solo puedes subir hasta 5 fotos del apartamento.")
        else:
            for photo in photos:
                try:
                    validate_image_extension(photo)
                except ValidationError as e:
                    photo_errors.append(e.message)

        for error in photo_errors:
            form.add_error(None, error)

        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.owner = request.user
            apartment.save()

            for photo in photos:
                ApartmentPhoto.objects.create(apartment=apartment, photo=photo)

            return redirect('owner_menu')

        return render(request, 'owner/apartment_form.html', {'form': form, 'edit_mode': False})

    form = ApartmentForm()
    return render(request, 'owner/apartment_form.html', {'form': form, 'edit_mode': False})

@login_required
@requires_role('owner')
def delete_apartment(request, apartment_id):
    try:
        apartment = Apartment.objects.get(id=apartment_id)

        if apartment.owner != request.user:
            return HttpResponseForbidden("No tienes permiso para eliminar este apartamento.")
    except Apartment.DoesNotExist:
        return redirect('owner_menu')

    if request.method == "POST":
        apartment.delete()
        return redirect('owner_menu')

    return redirect('owner_menu')

@login_required
@requires_role('owner')
def edit_apartment(request, apartment_id):
    if request.user.role != 'owner':
        return HttpResponseForbidden("No tienes permiso para editar apartamentos.")

    try:
        apartment = Apartment.objects.get(id=apartment_id)
    except Apartment.DoesNotExist:
        raise Http404("El apartamento no existe.")

    if apartment.owner != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este apartamento.")

    if request.method == 'POST':
        form = ApartmentForm(request.POST, instance=apartment)
        photos = request.FILES.getlist('photos')
        existing_photos = request.POST.getlist('existing_photos')
        photo_errors = []

        if not photos and not existing_photos:
            photo_errors.append("El apartamento debe tener al menos una foto.")
        elif (len(photos) + len(existing_photos)) > 5:
            photo_errors.append("Solo puedes subir hasta 5 fotos del apartamento.")
        else:
            for photo in photos:
                try:
                    validate_image_extension(photo)
                except ValidationError as e:
                    photo_errors.append(e.message)

        for error in photo_errors:
            form.add_error(None, error)

        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.owner = request.user
            apartment.save()

            # Elimina fotos no seleccionadas
            ApartmentPhoto.objects.filter(apartment=apartment).exclude(id__in=existing_photos).delete()

            # Guarda nuevas fotos
            for photo in photos:
                ApartmentPhoto.objects.create(apartment=apartment, photo=photo)

            messages.success(request, "Apartamento editado exitosamente.")
            return redirect('owner_menu')

        return render(request, 'owner/apartment_form.html', {
            'form': form,
            'apartment': apartment,
            'edit_mode': True,
        })

    form = ApartmentForm(instance=apartment)
    return render(request, 'owner/apartment_form.html', {
        'form': form,
        'apartment': apartment,
        'edit_mode': True,
    })

