from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, DetallePedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'reserva', 'valor_pagado', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'reserva': forms.Select(attrs={'class': 'form-select'}),
            'valor_pagado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cliente y reserva no son obligatorios
        self.fields['cliente'].required = False
        self.fields['reserva'].required = False
        # Valor pagado y estado se pueden inicializar en blanco
        self.fields['valor_pagado'].required = False
        self.fields['estado'].required = False


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el producto tiene un precio, se muestra automáticamente
        if self.instance and self.instance.producto:
            self.fields['precio_unitario'].initial = self.instance.producto.precio


# FormSet para manejar múltiples detalles de pedido
DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    form=DetallePedidoForm,
    extra=1,           # Muestra un formulario vacío adicional
    can_delete=True    # Permite eliminar filas de productos
)
