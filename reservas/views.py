from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm
from django.db.models import Q
from usuarios.decorators import rol_requerido


@rol_requerido(['admin', 'cajero', 'mesero'])
def lista_reservas(request):
    """
    Lista y filtra reservas por fecha, cliente o estado.
    """
    reservas = Reserva.objects.all().order_by('-fecha_reserva')

    # Captura de filtros desde la URL
    filtro_fecha = request.GET.get('fecha')
    estado = request.GET.get('estado')
    buscar = request.GET.get('buscar')

    # 🔹 Filtro por fecha
    if filtro_fecha:
        reservas = reservas.filter(fecha_reserva=filtro_fecha)

    # 🔹 Filtro por estado
    if estado and estado != "todos":
        reservas = reservas.filter(estado=estado)

    # 🔹 Búsqueda por nombre de cliente
    if buscar:
        reservas = reservas.filter(
            Q(cliente__nombre__icontains=buscar)
        )

    context = {
        'reservas': reservas,
        'filtro_fecha': filtro_fecha,
        'estado': estado,
        'buscar': buscar,
    }

    return render(request, 'reservas/lista_reservas.html', context)

@rol_requerido(['cajero', 'mesero'])
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva creada correctamente.")
            return redirect('reservas:lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/crear_reserva.html', {'form': form})


@rol_requerido(['admin', 'cajero'])
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva actualizada correctamente.")
            return redirect('reservas:lista_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/editar_reserva.html', {'form': form, 'reserva': reserva})


@rol_requerido(['admin', 'cajero', 'mesero'])
def cambiar_estado_reserva(request, id):
    """
    Permite cambiar el estado de una reserva (pendiente, confirmada, cancelada, completada)
    """
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        estados_validos = [e[0] for e in Reserva.ESTADOS]

        if nuevo_estado in estados_validos:
            reserva.estado = nuevo_estado
            reserva.save()
            messages.success(request, f"Estado actualizado a '{reserva.get_estado_display()}'.")
        else:
            messages.error(request, "Estado inválido seleccionado.")

        return redirect("reservas:lista_reservas")

    return render(request, "reservas/cambiar_estado.html", {"reserva": reserva})