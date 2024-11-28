from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from app.forms.CustomUserCreationForm import CustomUserCreationForm, CustomUserChangeForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from app.forms.EmailAuthenticationForm import EmailAuthenticationForm
from app.utils.correo import enviar_notificacion_correo

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()
            role = form.cleaned_data['role']  
            username = form.cleaned_data['username']
            
            if role == 'customer':
                mensaje = "Gracias "+ username+ " por registrarte en RentaHogar, como nuevo inquilino busca y disfruta de los mejores apartamentos al mejor precio."
            else:
                mensaje = "Gracias " + username+ " por registrarte en RentaHogar, como nuevo propietario, publica tus apartamentos y empieza a ganar dinero." 
                
            enviar_notificacion_correo("!BIENVENIDO a RentaHogar!", mensaje, form.cleaned_data['email'])
            
            return redirect('/auth/login/')

    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})



def user_login(request):    
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():

            user = form.get_user()
            login(request, user)

            if user.role == 'customer':
                return redirect('customer_menu')  
            elif user.role == 'owner':
                return redirect('owner_menu')  

    else:
        form = EmailAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def menu(request):
    
    user_role = request.user.role  # 'role' puede ser 'customer' o 'owner'
    
    if user_role == 'customer':
        return redirect('customer_menu')
    elif user_role == 'owner':
        return redirect('owner_menu')


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
    return redirect('/')

@login_required
def user_logout(request):
    logout(request)  
    return redirect('/')  