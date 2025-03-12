from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from app.models import *

class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['descripcion', 'cantidad']
        widgets={
            'descripcion': forms.TextInput(attrs={
                'placeholder': 'Descripción del elemento',
                'autofocus': True,
                'required': True,
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Cantidad',
                'autofocus': True,
                'required': True,
                'class': 'form-control',
            }),
        }
        
class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ['programa']
        widgets={
            'programa': forms.TextInput(attrs={
                'placeholder': 'Programa de formación',
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
            'programa', 'num_ficha', 'proyecto', 'instructor', 'aprendiz',
            'num_aprendices', 'num_contrato', 'obs_general', 'fecha_inicio_programa',
            'dependencia'
        ]
        widgets = {
            'programa': forms.Select(attrs={
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

class DetalleMovimientoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        for form in self.forms:
            if self.can_delete and form.cleaned_data.get('DELETE', False):
                continue

            cantidad_recibida = form.cleaned_data.get('cantidad_recibida', 0)
            cantidad_contratada = form.cleaned_data.get('cantidad_contratada', 0)

            if not cantidad_recibida and not cantidad_contratada:
                raise ValidationError(
                    "Debe especificar al menos una cantidad recibida o contratada en cada detalle."
                )
                
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
            'min': 1
        }),
        'cantidad_contratada': forms.NumberInput(attrs={
            'placeholder': 'Cantidad contratada',
            'required': True,
            'class': 'form-control',
            'min': 1
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
