from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre completo',
            'correo': 'Correo electrónico',
            'telefono': 'Teléfono',
            'activo': 'Cliente activo',
        }
