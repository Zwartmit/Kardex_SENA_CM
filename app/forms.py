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

class ElementoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Elemento
        fields = "__all__"
        widgets = {
            "elemento": TextInput(
                attrs={
                    "placeholder": "Nombre del elemento",
                }
            ),
            "cantidad": NumberInput(
                attrs={
                    "placeholder": "Cantidad a registrar",
                }
            ),
            "descripcion": TextInput(
                attrs={
                    "placeholder": "Descripción del elemento",
                }
            )
        }

class MovimientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Movimiento
        fields = ['elemento', 'tipo', 'cantidad']
        widgets = {
            'elemento': forms.Select(attrs={
                'class': 'form-control',
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Cantidad a registrar',
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