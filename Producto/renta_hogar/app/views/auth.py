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
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            if password_form.is_valid():
                user = form.save(commit=False)
                user.set_password(password_form.cleaned_data['new_password1'])  
                user.save()

                update_session_auth_hash(request, user)

                messages.success(request, '¡Tu perfil y contraseña se han actualizado correctamente!')
            else:
                form.save()
                messages.success(request, '¡Tu perfil se ha actualizado correctamente!')

            if request.user.role == 'customer':
                return redirect('customer_menu')
            elif request.user.role == 'owner':
                return redirect('owner_menu')
    else:
        form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'auth/edit_profile.html', {'form': form, 'password_form': password_form})


@login_required
def delete_account(request):
    request.user.delete()
    return redirect('home')

@login_required
def user_logout(request):
    logout(request)  
    return redirect('home')  