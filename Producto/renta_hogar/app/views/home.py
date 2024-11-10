# views.py

from django.shortcuts import render

def inicio(request):
    return render(request, 'home.html')  # Asegúrate de poner el nombre correcto de tu plantilla
