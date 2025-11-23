# panelAdmin/views.py

import json
from datetime import timedelta, date
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, F
from usuarios.decorators import rol_requerido
from django.db.models.functions import ExtractHour, TruncDate

from pedidos.models import Pedido, DetallePedido
from reservas.models import Reserva

@rol_requerido(['admin'])
def dashboard(request):
    # Fechas base
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    hace_7 = hoy - timedelta(days=6)

    # --- Capturar filtro GET (fecha_inicio, fecha_fin) ---
    fecha_inicio_str = request.GET.get("fecha_inicio")
    fecha_fin_str = request.GET.get("fecha_fin")
    fecha_inicio = None
    fecha_fin = None

    try:
        if fecha_inicio_str:
            fecha_inicio = date.fromisoformat(fecha_inicio_str)
        if fecha_fin_str:
            fecha_fin = date.fromisoformat(fecha_fin_str)
    except Exception:
        # Si la fecha enviada no es válida, ignoramos el filtro
        fecha_inicio = None
        fecha_fin = None

    # --- Totales generales (sin filtro) ---
    total_pedidos = Pedido.objects.count()
    pedidos_abiertos = Pedido.objects.filter(estado='ABIERTO').count()
    pedidos_pagados = Pedido.objects.filter(estado='PAGADO').count()
    ventas_totales = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0

    # --- Base de pedidos pagados (aplicar rango si existe) ---
    pedidos_pagados_qs = Pedido.objects.filter(estado='PAGADO')
    if fecha_inicio:
        pedidos_pagados_qs = pedidos_pagados_qs.filter(fecha_pedido__date__gte=fecha_inicio)
    if fecha_fin:
        pedidos_pagados_qs = pedidos_pagados_qs.filter(fecha_pedido__date__lte=fecha_fin)

    # Ventas totales dentro del rango (si no hay rango, será total de pagados)
    ventas_rango = pedidos_pagados_qs.aggregate(total=Sum('total'))['total'] or 0

    # --- Top 3 más vendidos y top 3 menos vendidos (desde DetallePedido filtrando por pedidos_pagados_qs) ---
    mas_vendidos_qs = (
        DetallePedido.objects
        .filter(pedido__in=pedidos_pagados_qs)
        .values('producto__id', 'producto__nombre')
        .annotate(total_cant=Sum('cantidad'))
        .order_by('-total_cant')[:3]
    )
    mas_vendidos = list(mas_vendidos_qs)

    menos_vendidos_qs = (
        DetallePedido.objects
        .filter(pedido__in=pedidos_pagados_qs)
        .values('producto__id', 'producto__nombre')
        .annotate(total_cant=Sum('cantidad'))
        .order_by('total_cant')[:3]
    )
    menos_vendidos = list(menos_vendidos_qs)

    # --- Hora con más reservas (usa hora_reserva: TimeField) ---
    hora_reservas = (
        Reserva.objects
        .annotate(hora=ExtractHour('hora_reserva'))
        .values('hora')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    hora_mas_reservas = hora_reservas.first()

    # --- Hora con más pedidos (usa fecha_pedido: DateTimeField) ---
    hora_pedidos = (
        Pedido.objects
        .annotate(hora=ExtractHour('fecha_pedido'))
        .values('hora')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    hora_mas_pedidos = hora_pedidos.first()

    # --- Ventas del mes y de la semana (si se aplica filtro, reflejará el rango) ---
    # Si hay filtro de fechas, calcular ventas en ese rango; si no, usar mes/semana por defecto.
    if fecha_inicio or fecha_fin:
        # ventas en el rango ya calculadas en ventas_rango
        ventas_mes = ventas_rango
        ventas_semana = ventas_rango
    else:
        ventas_mes = (
            Pedido.objects
            .filter(estado='PAGADO', fecha_pedido__date__gte=inicio_mes)
            .aggregate(total=Sum('total'))['total'] or 0
        )
        ventas_semana = (
            Pedido.objects
            .filter(estado='PAGADO', fecha_pedido__date__gte=inicio_semana)
            .aggregate(total=Sum('total'))['total'] or 0
        )

    # --- Contadores del mes (pedidos/reservas) (sin aplicar rango GET) ---
    pedidos_mes = Pedido.objects.filter(fecha_pedido__date__gte=inicio_mes).count()
    reservas_mes = Reserva.objects.filter(fecha_reserva__gte=inicio_mes).count()

    # --- Ventas últimos 7 días (respetando filtro si aplica) ---
    ventas_7_qs = (
        pedidos_pagados_qs
        .annotate(dia=TruncDate('fecha_pedido'))
        .values('dia')
        .annotate(total_dia=Sum('total'))
        .order_by('dia')
    )
    # crear mapa y lista de 7 días desde hace_7 hasta hoy
    ventas_map = {v['dia'].isoformat(): float(v['total_dia'] or 0) for v in ventas_7_qs}
    ventas_7_days = []
    for i in range(7):
        d = hace_7 + timedelta(days=i)
        ventas_7_days.append({
            "date": d.isoformat(),
            "value": ventas_map.get(d.isoformat(), 0.0)
        })

    # --- Últimos pedidos (independiente del filtro) ---
    ultimos = Pedido.objects.order_by('-fecha_pedido')[:5]
    ultimos_list = [
        {
            "id": p.id,
            "cliente": str(p.cliente) if p.cliente else "Sin cliente",
            "total": float(p.total or 0),
            "estado": p.estado,
            "fecha": p.fecha_pedido,
        }
        for p in ultimos
    ]

    context = {
        "total_pedidos": total_pedidos,
        "pedidos_abiertos": pedidos_abiertos,
        "pedidos_pagados": pedidos_pagados,
        "ventas_totales": ventas_totales,

        "producto_mas_vendido": mas_vendidos[0] if mas_vendidos else None,
        "mas_vendidos": mas_vendidos,
        "menos_vendidos": menos_vendidos,

        "hora_mas_reservas": hora_mas_reservas,
        "hora_mas_pedidos": hora_mas_pedidos,

        "ventas_mes": ventas_mes,
        "ventas_semana": ventas_semana,
        "ventas_rango": ventas_rango,
        "pedidos_mes": pedidos_mes,
        "reservas_mes": reservas_mes,

        "ventas_7_days_json": json.dumps(ventas_7_days),
        "ultimos_pedidos": ultimos_list,

        # para mantener controles en el template
        "fecha_inicio": fecha_inicio_str or "",
        "fecha_fin": fecha_fin_str or "",
    }

    return render(request, 'panelAdmin/panel.html', context)
