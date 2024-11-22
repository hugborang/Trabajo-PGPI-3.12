from django.shortcuts import render

def access_denied(request):
    return render(request, 'access_denied.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)


