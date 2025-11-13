from django.contrib import admin
from .models import Empleado

@admin.register(Empleado)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'rol', 'activo']
    list_filter = ['rol', 'activo']
    search_fields = ['nombre', 'codigo']
    ordering = ['codigo']