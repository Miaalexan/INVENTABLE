from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('editar/<int:id>/', views.editar_pedidos, name='editar_pedidos'),
    path('cambiar_estado/<int:id>/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pago/<int:id>/', views.pago_pedido, name='pago'),
]
