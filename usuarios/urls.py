from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registro_usuario, name='crear_usuario'),
    path('editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('activar/<int:id>/', views.activar_usuario, name='activar_usuario'),
    path('desactivar/<int:id>/', views.desactivar_usuario, name='desactivar_usuario'),
]
