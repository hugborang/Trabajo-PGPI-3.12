from django.shortcuts import render

def access_denied(request):
    return render(request, 'access_denied.html')
