from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout
from app.forms.CustomUserCreationForm import CustomUserCreationForm, CustomUserChangeForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


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



@login_required
def menu(request):
    
    user_role = request.user.role  # 'role' puede ser 'customer' o 'owner'
    
    if user_role == 'customer':
        return redirect('/customer_menu')
    elif user_role == 'owner':
        return redirect('/owner_menu')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            update_session_auth_hash(request, user)
            if user.role == 'customer':
                return redirect('/customer_menu')
            else:
                return redirect('/owner_menu')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'auth/edit_profile.html', {'form': form})



@login_required
def delete_account(request):
    request.user.delete()
    return redirect('home/search')

@login_required
def user_logout(request):
    logout(request)  
    return redirect('home/search')  