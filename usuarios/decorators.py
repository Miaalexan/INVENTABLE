from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            rol = request.session.get('rol')  # obtenemos el rol desde la sesión
            if rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para acceder a esta sección.")
            return redirect('usuarios:login')  # o 'home' si tienes una vista principal
        return wrapper
    return decorator
