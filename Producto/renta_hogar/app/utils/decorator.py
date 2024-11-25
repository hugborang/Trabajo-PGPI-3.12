from django.shortcuts import render

def requires_role(required_role):
    """
    Decorador que verifica el rol del usuario.
    Si no tiene el rol requerido, redirige a una página de acceso denegado.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and user.role != required_role:
                return render(request, 'access_denied.html', status=403)  
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
