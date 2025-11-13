from django.db import models

class Empleado(models.Model):
    ROLES = [
        ('admin', 'ADMIN'),
        ('cajero', 'CAJERO'),
        ('mesero', 'MESERO'),
    ]

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    rol = models.CharField(max_length=10, choices=ROLES)
    activo = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.nombre} ({self.rol}) - Código: {self.codigo}"
