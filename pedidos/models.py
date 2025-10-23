from django.db import models
from menu.models import Producto
from clientes.models import cliente
from reservas.models import reserva

# ==============================================================
# MÓDULO: MODELOS DEL PEDIDOS
# Este archivo define las clases (modelos) que representan la
# estructura de datos del menú dentro del sistema, es la estructura de la base de datos 
# ==============================================================

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)  # Para activar/desactivar
    
    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    nombre = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    num_personas = models.ForeignKey(reserva, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)  
    valor_pagado = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_pedido = models.DateTimeField(auto_now_add=True) 
    fecha_pago= models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
       return self.nombre
   
      