from django.shortcuts import render

def customer_menu(request):
    return render(request, 'customer/customer_menu.html')