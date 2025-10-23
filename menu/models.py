
from django.db import models

# ==============================================================
# MÓDULO: MODELOS DEL MENÚ
# Este archivo define las clases (modelos) que representan la
# estructura de datos del menú dentro del sistema, es la estructura de la base de datos 
# ==============================================================

class Categoria(models.Model):
       
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la categoría
    descripcion = models.TextField(blank=True, null=True)    # Descripción opcional
    
    def __str__(self):
        return self.nombre


"""
    Clase que representa un producto
    Cada producto pertenece a una categoría y tiene su propio precio 
    """
class Producto(models.Model):
    
    nombre= models.CharField(max_length=100)                            # Nombre del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)        # Precio con dos decimales
    descripcion = models.TextField(blank=True, null=True)                # Descripción opcional
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"