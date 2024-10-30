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
    
    def clean_item(self):
        item = self.cleaned_data.get('item')
        if item:
            item = item.capitalize()
            if Elemento.objects.filter(item__iexact=item).exists():
                raise forms.ValidationError('Ya existe un elemento con este nombre.')
        return item

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['descripcion', 'proyecto', 'num_ficha']  # Eliminados elemento y cantidad
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
        }

    def clean_num_ficha(self):
        num_ficha = self.cleaned_data.get('num_ficha')
        if num_ficha == '':
            raise forms.ValidationError('Este campo es obligatorio y no puede estar vacío.')
        return num_ficha


class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = ['elemento', 'cantidad']
        widgets = {
            'elemento': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Cantidad a registrar',
                'class': 'form-control',
            }),
        }
        
class ReporteForm(forms.Form):
    FORMATO_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, label='Formato del Reporte')