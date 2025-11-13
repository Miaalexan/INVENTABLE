from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','telefono','correo','direccion','activo')  # columnas que quieres ver en la lista
    search_fields = ('id', 'nombre','telefono','correo','direccion','activo')  # para habilitar búsqueda
    list_filter = ('id', 'nombre','telefono','correo','direccion','activo')  # filtros por categoría