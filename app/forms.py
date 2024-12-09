from django import forms
from django.forms import inlineformset_factory
from app.models import *

class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['descripcion']
        widgets={
            'descripcion': forms.TextInput(attrs={
                'placeholder': 'Descripción del elemento',
                'autofocus': True,
                'required': True,
                'class': 'form-control',
            }),
        }

class MovimientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Movimiento
        fields = [
            'programa_formacion', 'num_ficha', 'proyecto', 'instructor', 'aprendiz',
            'num_aprendices', 'num_contrato', 'obs_general', 'fecha_inicio_programa',
            'dependencia'
        ]
        widgets = {
            'programa_formacion': forms.Select(attrs={
                'placeholder': 'Programa de formación',
                'class': 'form-control',
            }),
            'num_ficha': forms.NumberInput(attrs={
                'placeholder': 'Número de ficha',
                'class': 'form-control',
                'autofocus': True,
                'min': 1,
            }),
            'proyecto': forms.Textarea(attrs={
                'placeholder': 'Proyectos asociados',
                'class': 'form-control',
                'rows': 3,
            }),
            'instructor': forms.TextInput(attrs={
                'placeholder': 'Nombre del instructor',
                'class': 'form-control',
            }),
            'aprendiz': forms.TextInput(attrs={
                'placeholder': 'Nombre del vocero',
                'class': 'form-control',
            }),
            'num_aprendices': forms.NumberInput(attrs={
                'placeholder': 'Número de aprendices',
                'class': 'form-control',
                'min': 1,
            }),
            'num_contrato': forms.NumberInput(attrs={
                'placeholder': 'Número del contrato',
                'class': 'form-control',
            }),
            'obs_general': forms.Textarea(attrs={
                'placeholder': 'Observaciones generales',
                'class': 'form-control',
                'rows': 3,
            }),
            'fecha_inicio_programa': forms.DateInput(attrs={
                'placeholder': 'Fecha de inicio del programa',
                'class': 'form-control',
                'type': 'date',
            }),
            'dependencia': forms.TextInput(attrs={
                'placeholder': 'Dependencia',
                'class': 'form-control',
            }),
        }

DetalleMovimientoFormSet = inlineformset_factory(
    Movimiento,
    DetalleMovimiento,
    fields=('elemento', 'cantidad_recibida', 'cantidad_contratada', 'saldo', 'observaciones'),
    widgets={
        'elemento': forms.Select(attrs={
            'placeholder': 'Elemento',
            'required': True,
            'class': 'form-control',
        }),
        'cantidad_recibida': forms.NumberInput(attrs={
            'placeholder': 'Cantidad recibida',
            'required': True,
            'class': 'form-control',
        }),
        'cantidad_contratada': forms.NumberInput(attrs={
            'placeholder': 'Cantidad contratada',
            'required': True,
            'class': 'form-control',
        }),
        'saldo': forms.NumberInput(attrs={
            'placeholder': 'Saldo pendiente de entrega',
            'required': True,
            'class': 'form-control',
        }),
        'observaciones': forms.TextInput(attrs={
            'placeholder': 'Observaciones',
            'required': True,
            'class': 'form-control',
        })
    },
    extra=1,
    can_delete=True,
)
