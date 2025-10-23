from django.db import models

# Create your models here.
# Atributos de la tabla

class Usuario(models.Model):
 Nombre=models.CharField(max_length=30)
 Nom_usuario=models.CharField(max_length=50)
 Cargo=models.CharField(max_length=30)
 Contrasenia=models.IntegerField(max_length=4) 
 
 def __str__(self):
     return self.Nombre
 
 def __str__(self):
     return self.Nom_usuario
 
 def __str__(self):
    return self.Cargo

def __str__(self):
    return self.Contrasenia


