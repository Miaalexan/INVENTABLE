from django.contrib import admin

from .models import Pedido
from .models import MetodoPago

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
  list_display = ('id','nombre','activo')
  search_fields = ('id', 'nombre','activo')
  list_filter = ('id', 'nombre','activo')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'valor_pagado', 'fecha_pedido', 'fecha_pago')  # columnas que quieres ver en la lista
    search_fields = ('id', 'total', 'valor_pagado', 'fecha_pedido', 'fecha_pago')  # para habilitar búsqueda
    list_filter = ('id', 'total', 'valor_pagado', 'fecha_pedido', 'fecha_pago')  # filtros por categoría
