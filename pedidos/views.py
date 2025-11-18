from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from pedidos.models import Pedido, DetallePedido
from menu.models import Categoria, Producto
from .forms import PedidoForm
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
        metodo_pago_id = request.POST.get("metodo_pago")

        productos_ids = request.POST.getlist("producto_id[]")
        cantidades = request.POST.getlist("cantidad[]")
        precios = request.POST.getlist("precio[]")

        if pedido_form.is_valid():

            # Crear pedido base
            pedido = pedido_form.save(commit=False)
            pedido.estado = "ABIERTO"
            pedido.total = 0
            pedido.save()

            total_final = 0

            # Crear detalles y calcular total
            for i in range(len(productos_ids)):
                producto = Producto.objects.get(id=productos_ids[i])
                cantidad = int(cantidades[i])
                precio = float(precios[i])

                subtotal = cantidad * precio
                total_final += subtotal

                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal
                )

            pedido.total = total_final

            # -----------------------------------
            #  PAGAR DIRECTAMENTE
            # -----------------------------------
            if metodo_pago_id:
                metodo_pago = Pedido.objects.get(id=metodo_pago_id)
                pedido.metodo_pago = metodo_pago
                pedido.estado = "PAGADO"
                pedido.valor_pagado = total_final
                pedido.fecha_pago = timezone.now()
                pedido.save()

                messages.success(request, "Pedido pagado correctamente.")
                return redirect('pedidos:lista_pedidos')

            # -----------------------------------
            #  SOLO GUARDAR
            # -----------------------------------
            pedido.save()

            messages.success(request, "Pedido guardado correctamente.")
            return redirect('pedidos:pago', pedido.id)

        else:
            messages.error(request, "Hay errores en el formulario.")

    else:
        pedido_form = PedidoForm()

    

    return render(request, 'pedidos/crear_pedido.html', {
        'pedido_form': pedido_form,
        'categorias': categorias,
        'metodos_pago': metodos
    })


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
#  CAMBIAR ESTADO
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
#  PANTALLA DE PAGO
# ======================================================
#rol_requerido(['admin', 'cajero'])
#def pago_pedido(request, id):
#   pedido = get_object_or_404(Pedido, id=id)
#
 #   if request.method == 'POST':
  #      metodo_id = request.POST.get('metodo')
#
 #       metodo = metodos_pago.objects.get(id=metodo_id)
  #      pedido.metodo_pago = metodo
   #     pedido.estado = 'PAGADO'
    #    pedido.fecha_pago = timezone.now()
     #   pedido.valor_pagado = pedido.total
      #  pedido.save()
#
 #       messages.success(request, f"Pedido #{pedido.id} pagado con {metodo.nombre}.")
  #      return redirect('pedidos:lista_pedidos')
#
 #   metodos_pago = metodos_pago.objects.filter(activo=True)
#
 #   context = {
  #      'pedido': pedido,
   #     'metodos_pago': metodos_pago,
    #}
   # return render(request, 'pedidos/lista_pedidos', context)
