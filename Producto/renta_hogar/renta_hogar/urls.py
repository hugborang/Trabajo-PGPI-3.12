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
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic.base import RedirectView
from app.views.auth import register, user_login, edit_profile, delete_account, menu, user_logout
from app.views.customers import customer_menu, manage_reservations
from app.views.owners import owner_menu, manage_availability, owner_reservations
from app.views.customers import customer_menu, manage_reservations
from app.views.owners import owner_menu, manage_availability
from django.conf import settings
from django.conf.urls.static import static
from app.views.apartment import delete_apartment, add_apartment, edit_apartment
from app.views.reservation import create_reservation, delete_reservation, verify_payment, delete_reservation_owner
from app.views.apartment import delete_apartment, add_apartment, edit_apartment, add_availability, delete_availability
from app.views.home import search_apartment
from app.views.error import access_denied
from app.views.review import create_reviews, apartment_review
from django.conf import settings
from django.conf.urls.static import static


app_name = 'app'


urlpatterns = [
    path('admin/', admin.site.urls),

    #Home
    path('home/search/', search_apartment, name='home_search'),
    path('access_denied/', access_denied, name='access_denied'),

      
    #Auths
    path('auth/register/', register, name='register'),  
    path('auth/login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('auth/edit_profile/', edit_profile, name='edit_profile'),
    path('auth/delete_account/', delete_account, name='delete_account'),
    path('auth/menu/', menu, name='menu'),


    #Customer
    path('customer_menu/', customer_menu, name='customer_menu'),
    path('manage_reservations/', manage_reservations, name='manage_reservations'),
    path('reservation/<int:apartment_id>/', create_reservation, name='create_reservation'),
    path('reservation/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('apartment/reviews/<int:apartment_id>/', create_reviews, name='create_review'),


    #Owner
    path('owner_menu/', owner_menu, name='owner_menu'),
    path('add_apartment/', add_apartment, name='add_apartment'),
    path('delete_apartment/<int:apartment_id>/', delete_apartment, name='delete_apartment'),
    path('edit_apartment/<int:apartment_id>/', edit_apartment, name='edit_apartment'),
    path('manage_availability/<int:apartment_id>/', manage_availability, name='manage_availability'),
    path('add_availability/<int:apartment_id>/', add_availability, name='add_availability'),
    path('delete_availability/<int:availability_id>/', delete_availability, name='delete_availability'),
    path('apartment/reviews/', apartment_review, name='owner_review'),
    path('owner_reservations/', owner_reservations, name='owner_reservations'),
    path('owner/reservation/delete/<int:reservation_id>/', delete_reservation_owner, name='delete_reservation_owner'),
   
    path('auth/menu/', menu, name='menu'),


    path('', RedirectView.as_view(url='home/search', permanent=False)),  # Ruta por defecto al iniciar la app


]



handler404='app.views.error.error_404'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
