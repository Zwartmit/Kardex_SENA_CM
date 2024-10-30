from django import forms
from django.forms import *
from app.models import *
from django import forms

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
        fields = ['num_ficha', 'proyecto', 'descripcion']
        widgets = {
            'num_ficha': forms.NumberInput(attrs={
                'placeholder': 'Número de ficha',
                'class': 'form-control',
            }),
            'proyecto': forms.TextInput(attrs={
                'placeholder': 'Nombre del proyecto',
                'class': 'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Descripción del movimiento',
                'class': 'form-control',
            }),
        }

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = Detalle_movimiento
        fields = ['elemento', 'cantidad']
        widgets = {
            'elemento': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un elemento',
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Cantidad a registrar',
                'class': 'form-control',
            }),
        }
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad

DetalleMovimientoFormSet = inlineformset_factory(Movimiento, Detalle_movimiento, form=DetalleMovimientoForm, extra=1)
    
class ReporteForm(forms.Form):
    FORMATO_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, label='Formato del Reporte')