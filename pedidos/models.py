from django.db import models
from menu.models import Producto
from clientes.models import Cliente
from reservas.models import Reserva
from django.utils import timezone

# ============================================================== 
# MODELOS DE PEDIDOS 
# ============================================================== 

class Pedido(models.Model):

    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    ]

    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True, blank=True)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, null=True, blank=True)
    valor_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ABIERTO')
   # fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.estado}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
         # Calcula el subtotal automáticamente
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - ${self.subtotal}"
