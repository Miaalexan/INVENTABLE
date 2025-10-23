from django.db import models
#importar el modelo 'Clientes'
from clientes.models import cliente


 #DEFINIR ESTADOS
ESTADO_CHOICES =(
    ('creada', 'Creada'),
    ('confirmada', 'Confirmada'),
    ('cancelada', 'Cancelada'),
    ('completada', 'Completada'),
    
)

# ATRIBUTOS DE MODELO
class reserva(models.Model):

 num_personas=models.IntegerField()
 fecha=models.DateField()
 hora=models.TimeField()
 cliente=models.ForeignKey(cliente, on_delete=models.CASCADE)
 estado=models.CharField(max_length=15, choices=ESTADO_CHOICES, default='creada')
 observaciones=models.TextField(blank=True)
 telefono=models.CharField(max_length=20)


def __str__(self):
    return self.num_personas
def __str__(self):
    return self.fecha
def __str__(self):
    return self.hora
def __str__(self):
    return self.cliente
def __str__(self):
    return self.estado
def __str__(self):
    return self.observaciones
def __str__(self):
    return self.telefono







