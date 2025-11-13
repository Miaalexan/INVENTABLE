from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200, blank=True, default='')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
