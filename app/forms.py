from dataclasses import fields
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget
from django import forms
from django.forms import *
from app.models import *
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Select, NumberInput, EmailInput, PasswordInput

class ElementoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Elemento
        fields = ['item', 'cantidad']
        widgets = {
            'item': forms.TextInput(attrs={
                'placeholder': 'Nombre del elemento',
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Cantidad a registrar',
                'class': 'form-control',
            })
        }

class MovimientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Movimiento
        fields = ['descripcion', 'proyecto', 'num_ficha', 'tipo']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Descripción del movimiento',
                'class': 'form-control',
            }),
            'proyecto': forms.TextInput(attrs={
                'placeholder': 'Nombre del proyecto',
                'class': 'form-control',
            }),
            'num_ficha': forms.NumberInput(attrs={
                'placeholder': 'Número de ficha',
                'class': 'form-control',
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        tipo = self.cleaned_data.get('tipo')
        elemento = self.cleaned_data.get('elemento')

        if tipo == 'salida' and elemento.cantidad < cantidad:
            raise forms.ValidationError("No hay suficiente stock para realizar la salida.")
        return cantidad

MovimientoFormSet = modelformset_factory(Movimiento, form=MovimientoForm, extra=1)

class ReporteForm(forms.Form):
    FORMATO_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, label='Formato del Reporte')