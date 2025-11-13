from django.shortcuts import render
from django.db.models import Sum, Count
from pedidos.models import Pedido, DetallePedido
from usuarios.decorators import rol_requerido
from datetime import datetime, timedelta
from usuarios.models import Empleado


@rol_requerido(['admin'])
def panel_administrativo(request):
    hoy = datetime.now().date()
    semana_inicio = hoy - timedelta(days=hoy.weekday())

   #definiendo usuario para que aparezca 
    usuario = None
    if request.session.get('usuario_id'):
        usuario = Empleado.objects.filter(id=request.session['usuario_id']).first()


    # 📊 Estadísticas básicas
    total_pedidos = Pedido.objects.count()
    pedidos_hoy = Pedido.objects.filter(fecha_pedido__date=hoy).count()
    ingresos_totales = Pedido.objects.aggregate(total=Sum('total'))['total'] or 0
    ingresos_semana = Pedido.objects.filter(fecha_pedido__date__gte=semana_inicio).aggregate(total=Sum('total'))['total'] or 0

    # 🛒 Productos más vendidos
    productos_top = (
        DetallePedido.objects
        .values('producto__nombre')
        .annotate(total_vendidos=Sum('cantidad'))
        .order_by('-total_vendidos')[:5]
    )

    # 📅 Ventas por día (últimos 7 días)
    ultimos_7_dias = []
    for i in range(7):
        dia = hoy - timedelta(days=i)
        total_dia = Pedido.objects.filter(fecha_pedido__date=dia).aggregate(total=Sum('total'))['total'] or 0
        ultimos_7_dias.append({'fecha': dia.strftime('%d/%m'), 'total': total_dia})
    ultimos_7_dias.reverse()

    contexto = {
        'usuario': usuario,
        'total_pedidos': total_pedidos,
        'pedidos_hoy': pedidos_hoy,
        'ingresos_totales': ingresos_totales,
        'ingresos_semana': ingresos_semana,
        'productos_top': productos_top,
        'ventas_dias': ultimos_7_dias,
    }

    return render(request, 'panelAdmin/panel.html', contexto)
