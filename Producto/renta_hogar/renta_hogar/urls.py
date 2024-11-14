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
from django.urls import path, include
from django.views.generic.base import RedirectView
from app.views.auth import register, user_login, user_logout, edit_profile
from app.views.auth import register, user_login, user_logout, edit_profile, delete_account, menu
from app.views.home import inicio
from app.views.customers import customer_menu, manage_reservations
from app.views.owners import owner_menu
from django.conf import settings
from django.conf.urls.static import static
from app.views import owners
from app.views.apartment import delete_apartment, add_apartment, edit_apartment, search_apartment
from app.views.reservation import create_reservation, delete_reservation

app_name = 'app'


urlpatterns = [
    path('admin/', admin.site.urls),

    #Auths
    path('auth/register/', register, name='register'),  
    path('auth/login/', user_login, name='login'),
    path('auth/logout/', user_logout, name='logout'),
    path('auth/edit_profile/', edit_profile, name='edit_profile'),
    path('auth/delete_account/', delete_account, name='delete_account'),
    path('auth/menu/', menu, name='menu'),
    #Home
    path('home/', search_apartment, name='home'),
    path('home/search/', search_apartment, name='home'),

    #Customer
    path('customer_menu/', customer_menu, name='customer_menu'),

    #Owner
    path('owner_menu/', owner_menu, name='owner_menu'),
    path('owner_menu/', owners.owner_menu, name='owner_menu'),
    path('add_apartment/', add_apartment, name='add_apartment'),
    path('', RedirectView.as_view(url='home/', permanent=False)),  # Ruta por defecto al iniciar la app
    path('delete_apartment/<int:apartment_id>/', delete_apartment, name='delete_apartment'),
    path('edit_apartment/<int:apartment_id>/', edit_apartment, name='edit_apartment'),
    path('manage_reservations/', manage_reservations, name='manage_reservations'),
    path('reservation/<int:apartment_id>/', create_reservation, name='create_reservation'),
    path('reservation/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('auth/menu/', menu, name='menu'),


    path('', RedirectView.as_view(url='home/', permanent=False)),  # Ruta por defecto al iniciar la app





]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
