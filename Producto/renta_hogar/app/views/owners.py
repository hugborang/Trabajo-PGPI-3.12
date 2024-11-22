from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Apartment 
from app.utils.decorator import requires_role  

@login_required
@requires_role('owner')
def owner_menu(request):
    apartments = Apartment.objects.filter(owner=request.user)
    return render(request, 'owner/owner_menu.html', {'apartments': apartments})
