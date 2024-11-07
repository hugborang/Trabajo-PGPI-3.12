"""
URL configuration for renta_hogar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from app.views.users import register, user_login 
from app.views.home import inicio
from app.views.book import reserva

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', register, name='register'),  
    path('auth/login/', user_login, name='login'),
    path('book/', reserva, name='book'),
    path('home/', inicio, name='home'),
    
    path('', RedirectView.as_view(url='home/', permanent=False)),  # Ruta por defecto al iniciar la app




]
