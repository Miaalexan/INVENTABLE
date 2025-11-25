from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path("pedidos/editar/<int:pedido_id>/", views.crear_pedido, name="editar_pedido"),
    path('cambiar_estado/<int:id>/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]
