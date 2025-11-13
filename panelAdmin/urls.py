from django.urls import path
from . import views

app_name = 'panelAdmin'

urlpatterns = [
    path('panel/', views.panel_administrativo, name='panel'),
]
