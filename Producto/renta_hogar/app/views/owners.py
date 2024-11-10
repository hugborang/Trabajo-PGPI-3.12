from django.shortcuts import render

def owner_menu(request):
    return render(request, 'owner/owner_menu.html')