from django import forms
from .models import Empleado

# crear usuario 
class UsuarioCreationForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'rol', 'codigo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
  
  #editar usuario       
class UsuarioChangeForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'rol', 'codigo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }