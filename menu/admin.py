# para ponerlo en el admin 

from django.contrib import admin
from menu.models import Producto
from menu.models import Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'nombre', 'precio')  # columnas que quieres ver en la lista
    search_fields = ('id', 'categoria', 'nombre', 'precio')  # para habilitar búsqueda
    list_filter = ('id', 'categoria', 'nombre', 'precio')  # filtros por categoría
    
    
@admin.register(Categoria)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')  # columnas que quieres ver en la lista
    search_fields = ('id', 'nombre', 'descripcion')  # para habilitar búsqueda
    list_filter = ('id', 'nombre', 'descripcion')  # filtros por categoría    