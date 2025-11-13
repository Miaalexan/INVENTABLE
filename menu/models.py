from django.db import models

# ==============================================================
# MÓDULO: MODELOS DEL MENÚ
# Este archivo define las clases (modelos) que representan la
# estructura de datos del menú dentro del sistema.
# ==============================================================

class Categoria(models.Model):
    """
    Representa una categoría dentro del menú (por ejemplo: Bebidas, Postres, Comidas).
    """
    nombre = models.CharField(max_length=100, unique=True)  # Nombre de la categoría
    descripcion = models.TextField(blank=True, null=True)    # Descripción opcional
    activo = models.BooleanField(default=True)     
    
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Representa un producto del menú.
    Cada producto pertenece a una categoría y tiene su propio precio.
    """
    nombre = models.CharField(max_length=100)                            # Nombre del producto
    descripcion = models.TextField(blank=True, null=True)                # Descripción opcional
    precio = models.DecimalField(max_digits=10, decimal_places=2)        # Precio con dos decimales
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')  
    activo = models.BooleanField(default=True)                           # Permite activar/desactivar el producto

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"
