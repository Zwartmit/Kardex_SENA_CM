from django import forms
from django.forms import *
from app.models import *
from django import forms

class ElementoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Elemento
        fields = ['item', 'cantidad_recibida', 'cantidad_contratada', 'unidad_medida', 'observaciones']
        widgets = {
            'item': forms.TextInput(attrs={
                'placeholder': 'Nombre del elemento',
                'class': 'form-control',
            }),
            'cantidad_recibida': forms.NumberInput(attrs={
                'placeholder': 'Cantidad recibida',
                'class': 'form-control',
                'min': 0,
            }),
            'cantidad_contratada': forms.NumberInput(attrs={
                'placeholder': 'Cantidad contratada',
                'class': 'form-control',
                'min': 0,
            }),
            'unidad_medida': forms.Textarea(attrs={
                'placeholder': 'Descripción',
                'class': 'form-control',
                'rows': 1,
            }),
            'observaciones': forms.Textarea(attrs={
                'placeholder': 'Observaciones',
                'class': 'form-control',
                'rows': 1,
            }),
        }
    
    def clean_item(self):
        item = self.cleaned_data.get('item')
        if item:
            item = item.capitalize()
            if Elemento.objects.filter(item__iexact=item).exists():
                raise ValidationError('Ya existe un elemento con este nombre.')
        return item

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'programa_formacion', 'num_ficha', 'proyecto', 'instructor', 'aprendiz', 
            'num_aprendices', 'num_contrato', 'obs_general', 'fecha_inicio_programa'
        ]
        widgets = {
            'programa_formacion': forms.Select(attrs={
                'placeholder': 'Nombre del programa',
                'class': 'form-control',
            }),
            'num_ficha': forms.NumberInput(attrs={
                'placeholder': 'Número de ficha',
                'class': 'form-control',
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
                'placeholder': 'Nombre del aprendiz',
                'class': 'form-control',
            }),
            'num_aprendices': forms.NumberInput(attrs={
                'placeholder': 'Número de aprendices',
                'class': 'form-control',
                'min': 1,
            }),
            'num_contrato': forms.NumberInput(attrs={
                'placeholder': 'Número de contrato',
                'class': 'form-control',
            }),
            'obs_general': forms.Textarea(attrs={
                'placeholder': 'Observaciones generales',
                'class': 'form-control',
            }),
            'fecha_inicio_programa': forms.DateInput(attrs={
                'placeholder': 'Fecha de inicio del programa',
                'class': 'form-control',
                'type': 'date',
            }),
        }

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = Detalle_movimiento
        fields = ['elemento', 'movimiento']
        widgets = {
            'elemento': forms.Select(attrs={'class': 'form-control'}),
            'movimiento': forms.Select(attrs={'class': 'form-control'}),
        }
    
DetalleMovimientoFormSet = inlineformset_factory(Movimiento, Detalle_movimiento, form=DetalleMovimientoForm, extra=1)
    
class ReporteForm(forms.Form):
    FORMATO_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, label='Formato del Reporte')