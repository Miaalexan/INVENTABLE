from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('estado/<int:id>/', views.estado_cliente, name='estado_cliente'),
]
