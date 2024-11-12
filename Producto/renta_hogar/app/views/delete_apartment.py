# delete_apartment.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from app.models import Apartment

def delete_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id, owner=request.user)
    if request.method == "POST":
        apartment.delete()
        messages.success(request, "Apartamento eliminado exitosamente.")
    return redirect('owner_menu')
