from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from pedidos.models import Pedido, DetallePedido
from menu.models import Categoria, Producto
from .forms import PedidoForm
from usuarios.decorators import rol_requerido
from django.db.models import Q


# ======================================================
# 📋 LISTA DE PEDIDOS
# ======================================================
@rol_requerido(['admin', 'cajero', 'mesero'])
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')

    # 🔹 Capturar filtros GET
    fecha = request.GET.get("fecha")
    buscar = request.GET.get("buscar")
    estado = request.GET.get("estado")

    # 🔹 Filtro por estado
    if estado:
        pedidos = pedidos.filter(estado=estado)

    # 🔹 Filtro por fecha exacta
    if fecha:
        pedidos = pedidos.filter(fecha_pedido__date=fecha)

    # 🔹 Filtro por texto (cliente o id)
    if buscar:
       pedidos = pedidos.filter(
        Q(id__icontains=buscar) |
        Q(cliente__nombre__icontains=buscar) 
    )


    return render(request, "pedidos/lista_pedidos.html", {
        "pedidos": pedidos,
        "fecha": fecha,
        "buscar": buscar,
        "estado": estado,
    })


# ======================================================
# 🆕 CREAR / EDITAR PEDIDO (Opción A)
# ======================================================
@rol_requerido(['admin', 'cajero', 'mesero'])
def crear_pedido(request, pedido_id=None):
    categorias = Categoria.objects.all()

    # ==================================================
    # 🔍 Si viene un pedido_id → estamos EDITANDO
    # ==================================================
    if pedido_id:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido_form = PedidoForm(request.POST or None, instance=pedido)
        detalles_existentes = DetallePedido.objects.filter(pedido=pedido)
        modo_edicion = True
    else:
        pedido = None
        pedido_form = PedidoForm(request.POST or None)
        detalles_existentes = []
        modo_edicion = False

    # ==================================================
    # 📝 Procesar formulario POST
    # ==================================================
    if request.method == "POST":

        accion = request.POST.get("accion")  # guardar o pagar

        if pedido_form.is_valid():

            pedido = pedido_form.save(commit=False)

            # Si es pagar → actualizar estado
            if accion == "pagar":
                pedido.estado = "PAGADO"
                pedido.fecha_pago = timezone.now()
                pedido.metodo_pago = request.POST.get("metodo_pago")

            pedido.total = 0
            pedido.save()

            # ---------------------------------------------
            #  🗑️ Si estamos editando → borrar detalles previos
            # ---------------------------------------------
            if modo_edicion:
                DetallePedido.objects.filter(pedido=pedido).delete()

            # ---------------------------------------------
            #  ➕ Guardar los nuevos detalles enviados
            # ---------------------------------------------
            productos = request.POST.getlist("producto_id[]")
            cantidades = request.POST.getlist("cantidad[]")
            precios = request.POST.getlist("precio[]")

            total_pedido = 0

            for i in range(len(productos)):
                cantidad = int(cantidades[i])
                precio = float(precios[i])
                subtotal = cantidad * precio

                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_id=productos[i],
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal
                )

                total_pedido += subtotal

            pedido.total = total_pedido
            pedido.save()

            # ---------------------------------------------
            #  Mensajes
            # ---------------------------------------------
            if accion == "guardar":
                messages.success(request, "Pedido guardado correctamente.")
            elif accion == "pagar":
                messages.success(request, "Pedido pagado con éxito.")

            return redirect("pedidos:lista_pedidos")

    # ==================================================
    #  📄 Renderizar formulario en crear o editar
    # ==================================================
    return render(request, "pedidos/crear_pedido.html", {
        "pedido_form": pedido_form,
        "categorias": categorias,
        "detalles_existentes": detalles_existentes,
        "modo_edicion": modo_edicion,
    })



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
