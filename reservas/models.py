from django.db import models
from clientes.models import Cliente

# ==============================================================
# MÓDULO: RESERVAS
# ==============================================================
class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_reserva = models.TimeField()
    num_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.cliente.nombre} - {self.fecha_reserva} ({self.estado})"
