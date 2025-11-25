# panelAdmin/views.py

import json
from datetime import timedelta, date, datetime, time
from decimal import Decimal

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, F, Avg
from usuarios.decorators import rol_requerido
from django.db.models.functions import ExtractHour, TruncDate, ExtractWeekDay
from django.db.models import Case, When, IntegerField

from pedidos.models import Pedido, DetallePedido
from reservas.models import Reserva


# ---------------------------------------------------------
#     FUNCIÓN PARA SERIALIZAR DECIMAL, DATE, TIME, ETC.
# ---------------------------------------------------------
def safe_json(data):
    """Convierte tipos no serializables (Decimal, date, time) a tipos válidos para JSON."""
    if isinstance(data, list):
        return [safe_json(item) for item in data]
    if isinstance(data, dict):
        return {key: safe_json(value) for key, value in data.items()}
    if isinstance(data, Decimal):
        return float(data)
    if isinstance(data, (date, datetime, time)):
        return str(data)
    return data


# ---------------------------------------------------------
#                 DASHBOARD PRINCIPAL
# ---------------------------------------------------------
@rol_requerido(['admin'])
def dashboard(request):

    # Fechas base
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    hace_7 = hoy - timedelta(days=6)

    # Filtros GET
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
        fecha_inicio = None
        fecha_fin = None

    # ---- Totales generales ----
    total_pedidos = Pedido.objects.count()
    pedidos_abiertos = Pedido.objects.filter(estado='ABIERTO').count()
    pedidos_pagados = Pedido.objects.filter(estado='PAGADO').count()
    ventas_totales = Pedido.objects.aggregate(suma_total=Sum('total'))['suma_total'] or 0

    # Pedidos pagados con filtro
    pedidos_pagados_qs = Pedido.objects.filter(estado='PAGADO')

    if fecha_inicio:
        pedidos_pagados_qs = pedidos_pagados_qs.filter(fecha_pedido__date__gte=fecha_inicio)
    if fecha_fin:
        pedidos_pagados_qs = pedidos_pagados_qs.filter(fecha_pedido__date__lte=fecha_fin)

    ventas_rango = pedidos_pagados_qs.aggregate(suma_total=Sum('total'))['suma_total'] or 0

    # ---- Más vendidos / menos vendidos ----
    mas_vendidos = list(
        DetallePedido.objects
        .filter(pedido__in=pedidos_pagados_qs)
        .values('producto__id', 'producto__nombre')
        .annotate(total_cant=Sum('cantidad'))
        .order_by('-total_cant')[:3]
    )

    menos_vendidos = list(
        DetallePedido.objects
        .filter(pedido__in=pedidos_pagados_qs)
        .values('producto__id', 'producto__nombre')
        .annotate(total_cant=Sum('cantidad'))
        .order_by('total_cant')[:3]
    )

    # Top 10 productos
    top_10_productos = list(
        DetallePedido.objects
        .filter(pedido__in=pedidos_pagados_qs)
        .values('producto__nombre')
        .annotate(total_cant=Sum('cantidad'))
        .order_by('-total_cant')[:10]
    )

    # ---- Métricas de horas ----
    hora_mas_reservas = (
        Reserva.objects
        .annotate(hora=ExtractHour('hora_reserva'))
        .values('hora')
        .annotate(total_reservas=Count('id'))
        .order_by('-total_reservas')
    ).first()

    hora_mas_pedidos = (
        Pedido.objects
        .annotate(hora=ExtractHour('fecha_pedido'))
        .values('hora')
        .annotate(total_pedidos=Count('id'))
        .order_by('-total_pedidos')
    ).first()

    # ---- Ventas mes / semana ----
    if fecha_inicio or fecha_fin:
        ventas_mes = ventas_rango
        ventas_semana = ventas_rango
    else:
        ventas_mes = Pedido.objects.filter(
            estado='PAGADO',
            fecha_pedido__date__gte=inicio_mes
        ).aggregate(suma_total=Sum('total'))['suma_total'] or 0

        ventas_semana = Pedido.objects.filter(
            estado='PAGADO',
            fecha_pedido__date__gte=inicio_semana
        ).aggregate(suma_total=Sum('total'))['suma_total'] or 0

    pedidos_mes = Pedido.objects.filter(fecha_pedido__date__gte=inicio_mes).count()
    reservas_mes = Reserva.objects.filter(fecha_reserva__gte=inicio_mes).count()

    # ---- Ventas últimos 7 días ----
    ventas_7_qs = (
        pedidos_pagados_qs
        .annotate(dia=TruncDate('fecha_pedido'))
        .values('dia')
        .annotate(total_dia=Sum('total'))
        .order_by('dia')
    )

    ventas_map = {str(v['dia']): float(v['total_dia']) for v in ventas_7_qs}

    ventas_7_days = []
    for i in range(7):
        d = hace_7 + timedelta(days=i)
        ventas_7_days.append({
            "date": str(d),
            "value": ventas_map.get(str(d), 0)
        })

    # Últimos pedidos
    ultimos_list = [
        {
            "id": p.id,
            "cliente": str(p.cliente) if p.cliente else "Sin cliente",
            "total": float(p.total or 0),
            "estado": p.estado,
            "fecha": str(p.fecha_pedido),
        }
        for p in Pedido.objects.order_by('-fecha_pedido')[:5]
    ]

    # ----------- NUEVAS MÉTRICAS (TAL COMO ESTABAN) ----------------

    top_clientes_frecuencia = list(
        Pedido.objects
        .filter(estado='PAGADO')
        .values('cliente__id', 'cliente__nombre')
        .annotate(total_pedidos=Count('id'))
        .order_by('-total_pedidos')[:5]
    )

    top_clientes_gasto = list(
        Pedido.objects
        .filter(estado='PAGADO')
        .values('cliente__id', 'cliente__nombre')
        .annotate(total_gastado=Sum('total'))
        .order_by('-total_gastado')[:5]
    )

    total_clientes_unicos = Pedido.objects.values('cliente').distinct().count()

    ticket_promedio = (
        Pedido.objects.filter(estado='PAGADO')
        .aggregate(promedio=Avg('total'))['promedio'] or 0
    )

    ventas_por_categoria = list(
        DetallePedido.objects
        .filter(pedido__estado='PAGADO')
        .values('producto__categoria__nombre')
        .annotate(
            total_ventas=Sum(F('cantidad') * F('precio_unitario')),
            cantidad_vendida=Sum('cantidad')
        )
        .order_by('-total_ventas')
    )

    reservas_por_dia_semana = list(
        Reserva.objects
        .annotate(dia_semana=ExtractWeekDay('fecha_reserva'))
        .values('dia_semana')
        .annotate(total_reservas=Count('id'))
        .order_by('dia_semana')
    )

    pedidos_heatmap = list(
        Pedido.objects
        .filter(estado='PAGADO')
        .annotate(
            dia_semana=ExtractWeekDay('fecha_pedido'),
            hora=ExtractHour('fecha_pedido')
        )
        .values('dia_semana', 'hora')
        .annotate(total_pedidos=Count('id'))
        .order_by('dia_semana', 'hora')
    )

    productos_por_turno = list(
        DetallePedido.objects
        .filter(pedido__estado='PAGADO')
        .annotate(
            hora=ExtractHour('pedido__fecha_pedido'),
            turno=Case(
                When(hora__gte=6, hora__lt=12, then=1),
                When(hora__gte=12, hora__lt=18, then=2),
                When(hora__gte=18, hora__lt=24, then=3),
                default=1,
                output_field=IntegerField()
            )
        )
        .values('turno')
        .annotate(
            total_vendido=Sum('cantidad'),
            total_ingresos=Sum(F('cantidad') * F('precio_unitario'))
        )
        .order_by('turno')
    )

    for turno in productos_por_turno:
        if turno["turno"] == 1:
            turno["nombre_turno"] = "Mañana"
        elif turno["turno"] == 2:
            turno["nombre_turno"] = "Tarde"
        else:
            turno["nombre_turno"] = "Noche"

    # Días de la semana
    pedidos_por_dia_semana = list(
        Pedido.objects
        .filter(estado='PAGADO')
        .annotate(dia_semana=ExtractWeekDay('fecha_pedido'))
        .values('dia_semana')
        .annotate(
            total_pedidos=Count('id'),
            total_ventas=Sum('total')
        )
        .order_by('dia_semana')
    )

    dias_nombres = {
        1: 'Domingo', 2: 'Lunes', 3: 'Martes',
        4: 'Miércoles', 5: 'Jueves', 6: 'Viernes', 7: 'Sábado'
    }

    for dia in pedidos_por_dia_semana:
        dia['nombre_dia'] = dias_nombres.get(dia['dia_semana'], 'Desconocido')

    context = {

        "total_pedidos": total_pedidos,
        "pedidos_abiertos": pedidos_abiertos,
        "pedidos_pagados": pedidos_pagados,
        "ventas_totales": ventas_totales,

        "producto_mas_vendido": mas_vendidos[0] if mas_vendidos else None,
        "mas_vendidos": mas_vendidos,
        "menos_vendidos": menos_vendidos,
        "top_10_productos": top_10_productos,

        "hora_mas_reservas": hora_mas_reservas,
        "hora_mas_pedidos": hora_mas_pedidos,

        "ventas_mes": ventas_mes,
        "ventas_semana": ventas_semana,
        "ventas_rango": ventas_rango,
        "pedidos_mes": pedidos_mes,
        "reservas_mes": reservas_mes,

        "ventas_7_days_json": json.dumps(safe_json(ventas_7_days)),
        "ultimos_pedidos": ultimos_list,

        "fecha_inicio": fecha_inicio_str or "",
        "fecha_fin": fecha_fin_str or "",

        # Clientes
        "top_clientes_frecuencia": top_clientes_frecuencia,
        "top_clientes_gasto": top_clientes_gasto,
        "total_clientes_unicos": total_clientes_unicos,
        "ticket_promedio": float(ticket_promedio),

        # Categorías
        "ventas_por_categoria": ventas_por_categoria,
        "ventas_por_categoria_json": json.dumps(safe_json(ventas_por_categoria)),

        # Reservas
        "reservas_por_dia_semana": reservas_por_dia_semana,
        "reservas_por_dia_semana_json": json.dumps(safe_json(reservas_por_dia_semana)),

        # Heatmap
        "pedidos_heatmap_json": json.dumps(safe_json(pedidos_heatmap)),

        # Turnos
        "productos_por_turno": productos_por_turno,
        "productos_por_turno_json": json.dumps(safe_json(productos_por_turno)),

        # Días semana
        "pedidos_por_dia_semana": pedidos_por_dia_semana,
        "pedidos_por_dia_semana_json": json.dumps(safe_json(pedidos_por_dia_semana)),
    }

    return render(request, 'panelAdmin/panel.html', context)
