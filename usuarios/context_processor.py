from usuarios.models import Empleado

def usuario_logeado(request):
    """
    Retorna el usuario del sistema basado en tu modelo personalizado 'Usuario'.
    Esto estará disponible en TODAS las plantillas como: {{ usuario }}
    """
    if request.user.is_authenticated:
        try:
            usuario = Empleado.objects.get(id=request.user.id)
            return {"usuario": usuario}
        except Empleado.DoesNotExist:
            return {"usuario": None}

    return {"usuario": None}
