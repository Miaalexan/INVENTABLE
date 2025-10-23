from django.urls import path
from . import views

# ---------------------------------------------------------
# RUTAS DEL MÓDULO "MENÚ"

# Este archivo define las rutas (URLs) que permiten acceder
# a las vistas del módulo desde el navegador.
#
# RUTAS DESTINADAS:
# - /menu/  -> Lista todos los productos
# - /menu/New/  -> Crea un nuevo producto
# - /menu/edit/1/  -> Edita el producto con ID 1
# - /menu/eliminar/1/ -> Elimina el producto con ID 1
# ---------------------------------------------------------

app_name = 'menu'

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('New/', views.crear_producto, name='crear_producto'),
    path('edit/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]
