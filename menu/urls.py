from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('estado/<int:id>/', views.cambiar_estado_producto, name='cambiar_estado_producto'),
]