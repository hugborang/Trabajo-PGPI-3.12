# views.py

from django.shortcuts import render

def reserva(request):
    return render(request, 'book.html')  # Asegúrate de poner el nombre correcto de tu plantilla
