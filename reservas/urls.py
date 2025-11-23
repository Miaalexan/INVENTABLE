from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.lista_reservas, name='lista_reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
     path('estado/<int:id>/', views.cambiar_estado_reserva, name='cambiar_estado_reserva'),
    path('editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
]
