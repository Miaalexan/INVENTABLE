from django import forms
from menu.models import Producto

class ProductoForm(forms.ModelForm):
    """
    Forms se utiliza para crear o editar productos
    dentro del sistema (en el módulo del menú).
    """

    class Meta:
        model = Producto  # Indica que el formulario usa el modelo Producto
        fields = ['nombre', 'categoria', 'precio']  # Campos que aparecerán en el formulario

        # Personalización de etiquetas y widgets (opcional pero recomendado)
        labels = {
            'nombre': 'Nombre del producto',
            'categoria': 'Categoría',
            'precio': 'Precio (COP)',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pizza Hawaiana'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Bebida, Comida...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
