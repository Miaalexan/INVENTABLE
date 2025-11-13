from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    """
    Formulario para crear o editar productos del menú.
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional'}),
        }
