from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from app.forms.CustomUserCreationForm import CustomUserCreationForm  

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('/auth/login/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            if user.role == 'customer':
                return redirect('/customer_menu')  
            elif user.role == 'owner':
                return redirect('/owner_menu')  
            
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})



def user_logout(request):
    logout(request)  
    return redirect('home')  