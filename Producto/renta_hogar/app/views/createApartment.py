from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.forms.Apartmentform import ApartmentForm
from app.models import Apartment, ApartmentPhoto

@login_required
def add_apartment(request):
    if request.user.role != 'owner':
        messages.error(request, "No tienes permiso para añadir apartamentos.")
        return redirect('owner_menu')  # Redirige al menú del propietario

    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        photos = request.FILES.getlist('photos')  # Obtener las fotos de los archivos subidos

        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.owner = request.user
            apartment.save()

            # Guardar cada foto asociada al apartamento
            for photo in photos:
                ApartmentPhoto.objects.create(apartment=apartment, photo=photo)

            messages.success(request, "Apartamento añadido exitosamente.")
            return redirect('owner_menu')
    else:
        form = ApartmentForm()

    return render(request, 'owner/add_apartment.html', {'form': form})

