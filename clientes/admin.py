from django.contrib import admin
from .models import cliente


@admin.register(cliente)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'num_documento','telefono','correo')  # columnas que quieres ver en la lista
    search_fields = ('id', 'nombre', 'apellido', 'num_documento','telefono','correo')  # para habilitar búsqueda
    list_filter = ('id', 'nombre', 'apellido', 'num_documento','telefono','correo')  # filtros por categoría