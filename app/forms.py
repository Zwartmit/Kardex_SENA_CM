from django import forms
from django.forms import inlineformset_factory
from app.models import *

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
                'min': 1,
            }),
            'proyecto': forms.Textarea(attrs={
                'placeholder': 'Proyectos',
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
                'placeholder': 'Observaciones',
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
ElementoFormSet = inlineformset_factory(
    Movimiento,
    Elemento,
    fields=['item', 'descripcion', 'cantidad_recibida', 'cantidad_contratada', 'saldo', 'observaciones'],
    widgets={
        'item': forms.TextInput(attrs={
            'placeholder': 'Ítem',
            'required': True,
            'class': 'form-control',
        }),
        'descripcion': forms.TextInput(attrs={
            'placeholder': 'Descripción del elemento',
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
    extra=1,  # Número de formularios vacíos adicionales para agregar
    can_delete=True  # Permite eliminar elementos
)

class ReporteForm(forms.Form):
    FORMATO_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, label='Formato del Reporte')
