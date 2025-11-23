from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Empleado
from .forms import UsuarioChangeForm, UsuarioCreationForm
from usuarios.decorators import rol_requerido



# --- LOGIN ---
def login_usuario(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            usuario = Empleado.objects.get(codigo=codigo, activo=True)
            # Guardar info mínima en sesión
            request.session['usuario_id'] = usuario.id
            request.session['rol'] = usuario.rol
            request.session['nombre'] = usuario.nombre
            messages.success(request, f"Bienvenido {usuario.nombre}")
            return redirect('usuarios:inicio')
        except Empleado.DoesNotExist:
            messages.error(request, "Código inválido o usuario inactivo.")
    

    return render(request, 'usuarios/login.html')


# --- LOGOUT ---
def logout_usuario(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('usuarios:login')


# --- INICIO (solo para usuarios logueados) ---
@rol_requerido(['admin', 'cajero', 'mesero'])
def inicio(request):
    nombre = request.session.get('nombre')
    rol = request.session.get('rol')
    return render(request, 'pedidos/lista_pedidos.html', {'nombre': nombre, 'rol': rol})


# --- LISTA DE USUARIOS (solo admin) ---
@rol_requerido(['admin'])
def lista_usuarios(request):
    usuarios = Empleado.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


# --- CREAR USUARIO (solo admin) ---
@rol_requerido(['admin'])
def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


# --- EDITAR USUARIO (solo admin) ---
@rol_requerido(['admin'])
def editar_usuario(request, id):
    usuario = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('usuarios:lista_usuarios')
    else:
        form = UsuarioChangeForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})
@rol_requerido(['admin'])
def activar_usuario(request, id):
    usuario = get_object_or_404(Empleado, id=id)
    usuario.activo = True
    usuario.save()
    messages.success(request, f"Usuario {usuario.nombre} ha sido activado correctamente.")
    return redirect('usuarios:lista_usuarios')


@rol_requerido(['admin'])
def desactivar_usuario(request, id):
    usuario = get_object_or_404(Empleado, id=id)
    usuario.activo = False
    usuario.save()
    messages.warning(request, f"Usuario {usuario.nombre} ha sido desactivado.")
    return redirect('usuarios:lista_usuarios')