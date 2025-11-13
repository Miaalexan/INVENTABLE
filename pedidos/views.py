from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Pedido, DetallePedido
from menu.models import Categoria, Producto
from .forms import PedidoForm, DetallePedidoFormSet
from usuarios.decorators import rol_requerido

# ======================================================
# 📋 LISTA DE PEDIDOS
# ======================================================
@rol_requerido(['admin', 'cajero', 'mesero'])
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')

    filtro = request.GET.get('filtro')
    if filtro == 'abiertas':
        pedidos = pedidos.filter(estado='ABIERTO')
    elif filtro == 'hoy':
        pedidos = pedidos.filter(fecha_pedido__date=timezone.now().date())

    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})


# ======================================================
# 🆕 CREAR PEDIDO
# ======================================================
@rol_requerido(['admin', 'cajero', 'mesero'])
def crear_pedido(request):
    categorias = Categoria.objects.prefetch_related('productos').all()

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        formset = DetallePedidoFormSet(request.POST)

        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.total = 0
            pedido.estado = 'ABIERTO'
            pedido.save()

            formset.instance = pedido
            formset.save()

            # Calcula total
            total = pedido.detalles.aggregate(total=Sum('subtotal'))['total'] or 0
            pedido.total = total
            pedido.save()

            messages.success(request, "Pedido creado correctamente.")
            return redirect('pedidos:pago', pedido.id)
        else:
            messages.error(request, "Hay errores en el formulario.")
    else:
        pedido_form = PedidoForm()
        formset = DetallePedidoFormSet()

    context = {
        'pedido_form': pedido_form,
        'formset': formset,
        'categorias': categorias,
    }
    return render(request, 'pedidos/crear_pedido.html', context)


# ======================================================
# ✏️ EDITAR PEDIDO
# ======================================================
@rol_requerido(['admin', 'cajero'])
def editar_pedidos(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido actualizado correctamente.")
            return redirect('pedidos:lista_pedidos')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'pedidos/editar_pedidos.html', {'form': form, 'pedido': pedido})


# ======================================================
# 🔁 CAMBIAR ESTADO
# ======================================================
@rol_requerido(['admin', 'cajero', 'mesero'])
def cambiar_estado_pedido(request, id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = nuevo_estado

    if nuevo_estado == 'PAGADO':
        pedido.fecha_pago = timezone.now()

    pedido.save()
    messages.success(request, f"El pedido #{pedido.id} cambió su estado a {nuevo_estado}.")
    return redirect('pedidos:lista_pedidos')


# ======================================================
# 💵 PANTALLA DE PAGO
# ======================================================
@rol_requerido(['admin', 'cajero'])
def pago_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == 'POST':
        metodo = request.POST.get('metodo')
        pedido.metodo_pago = metodo
        pedido.estado = 'PAGADO'
        pedido.fecha_pago = timezone.now()
        pedido.valor_pagado = pedido.total
        pedido.save()

        messages.success(request, f"Pedido #{pedido.id} pagado con {metodo}.")
        return redirect('pedidos:lista_pedidos')

    metodos_pago = [
        ('Efectivo', 'bi-cash'),
        ('Tarjeta', 'bi-credit-card-2-front'),
        ('Transferencia', 'bi-bank'),
        ('Nequi', 'bi-phone'),
    ]

    context = {
        'pedido': pedido,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'pedidos/pago.html', context)
