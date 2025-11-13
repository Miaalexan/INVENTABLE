from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from django.db.models import Q


# Lista de clientes con búsqueda y filtro
def lista_clientes(request):
    # Obtener parámetros de búsqueda y filtro
    busqueda = request.GET.get('buscar', '')
    filtro_estado = request.GET.get('estado', 'todos')
    
    # Consulta base
    clientes = Cliente.objects.all()
    
    # Aplicar búsqueda por nombre, correo o teléfono
    if busqueda:
        clientes = clientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(correo__icontains=busqueda) |
            Q(telefono__icontains=busqueda)
        )
    
    # Aplicar filtro de estado
    if filtro_estado == 'activos':
        clientes = clientes.filter(activo=True)
    elif filtro_estado == 'inactivos':
        clientes = clientes.filter(activo=False)
    
    # Ordenar por nombre
    clientes = clientes.order_by('nombre')
    
    contexto = {
        'clientes': clientes,
        'busqueda': busqueda,
        'filtro_estado': filtro_estado,
        'total_clientes': clientes.count(),
    }
    
    return render(request, 'clientes/lista_clientes.html', contexto)

#crear cliente 
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_clientes.html', {'form': form})

# editar cliente 
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_clientes.html', {'form': form})


def estado_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.activo = not cliente.activo
    cliente.save()

    estado = "activado" if cliente.activo else "desactivado"
    messages.success(request, f"El cliente {cliente.nombre} ha sido {estado} correctamente.")
    
    return redirect('clientes:lista_clientes')