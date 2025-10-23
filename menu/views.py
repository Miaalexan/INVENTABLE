from django.shortcuts import render, redirect, get_object_or_404
from menu.models import Producto
from .forms import ProductoForm


def lista_productos(request):
    """
    Muestra todos los productos registrados en el sistema.
    """
    productos = Producto.objects.all()
    return render(request, 'menu/lista_productos.html', {'productos': productos})


def crear_producto(request):
    """
    Permite registrar un nuevo producto mediante un formulario.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a la vista de lista
    else:
        form = ProductoForm()
    return render(request, 'menu/crear_producto.html', {'form': form})



def editar_producto(request, id):
    """
    Permite editar la información de un producto existente.
    """
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'menu/editar_producto.html', {'form': form})



def eliminar_producto(request, id):
    """
    Permite eliminar un producto del sistema.
    """
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'menu/eliminar_producto.html', {'producto': producto})
