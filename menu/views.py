from django.shortcuts import render, redirect, get_object_or_404
from menu.models import Producto, Categoria
from .forms import ProductoForm
from django.contrib import messages


# ==============================
# VISTAS DEL MENÚ
# ==============================

def lista_productos(request):
    """
    Muestra los productos con filtros por nombre y categoría.
    """
    categorias = Categoria.objects.all().order_by('nombre')
    productos = Producto.objects.select_related('categoria').all()

    # Capturar parámetros GET
    buscar_producto = request.GET.get('buscar_producto')
    buscar_categoria = request.GET.get('buscar_categoria')

    #  Filtro por nombre de producto
    if buscar_producto:
        productos = productos.filter(nombre__icontains=buscar_producto)

    #  Filtro por nombre de categoría 
    if buscar_categoria:
        productos = productos.filter(categoria__nombre__icontains=buscar_categoria)

    context = {
        'categorias': categorias,
        'productos': productos,
        'buscar_producto': buscar_producto,
        'buscar_categoria': buscar_categoria,
    }

    return render(request, 'menu/lista_productos.html', context)


# ==============================
# CREAR PRODUCTO
# ==============================
def crear_producto(request):
    """
    Permite registrar un nuevo producto mediante un formulario.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('menu:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'menu/crear_producto.html', {'form': form})


# ==============================
# EDITAR PRODUCTO
# ==============================
def editar_producto(request, id):
    """
    Permite editar la información de un producto existente.
    """
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('menu:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'menu/editar_producto.html', {'form': form})


# ==============================
# CAMBIAR ESTADO PRODUCTO
# ==============================
def cambiar_estado_producto(request, id):
    """
    Activa o desactiva un producto sin eliminarlo.
    """
    producto = get_object_or_404(Producto, id=id)
    producto.activo = not producto.activo  # Cambia el estado (True ↔ False)
    producto.save()

    estado = "activado" if producto.activo else "desactivado"
    messages.info(request, f'El producto "{producto.nombre}" fue {estado}.')
    return redirect('menu:lista_productos')


# ==============================
# CREAR CATEGORÍA
# ==============================
def crear_categoria(request):
    """
    Permite crear una nueva categoría desde un formulario.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Validar que no exista una categoría con el mismo nombre
        if Categoria.objects.filter(nombre__iexact=nombre).exists():
            messages.warning(request, f'Ya existe una categoría con el nombre "{nombre}".')
        else:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, f'La categoría "{nombre}" fue creada correctamente.')
            return redirect('menu:lista_productos')

    return render(request, 'menu/crear_categoria.html')
