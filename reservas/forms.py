from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'fecha_reserva', 'hora_reserva', 'num_personas', 'estado', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha_reserva': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_reserva': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'num_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
