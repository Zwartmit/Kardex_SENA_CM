from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget
from app.models import Elemento, Movimiento, DetalleMovimiento

class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['item', 'saldo', 'cantidad_recibida', 'cantidad_contratada', 'descripcion', 'observaciones']
        widgets = {
            'item': forms.TextInput(attrs={
                'placeholder': 'Nombre del elemento',
                'class': 'form-control',
            }),
            'saldo': forms.NumberInput(attrs={
                'placeholder': 'Saldo del elemento',
                'class': 'form-control',
                'min': 0,
            }),
            'cantidad_recibida': forms.NumberInput(attrs={
                'placeholder': 'Cantidad recibida',
                'class': 'form-control',
                'min': 1,
            }),
            'cantidad_contratada': forms.NumberInput(attrs={
                'placeholder': 'Cantidad contratada',
                'class': 'form-control',
                'min': 1,
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Descripción del elemento',
                'class': 'form-control',
                'rows': 3,
            }),
            'observaciones': forms.Textarea(attrs={
                'placeholder': 'Observaciones sobre el elemento',
                'class': 'form-control',
                'rows': 3,
            }),
        }

    def clean_item(self):
        item = self.cleaned_data.get('item')
        if item:
            item = item.capitalize()
            if Elemento.objects.filter(item__iexact=item).exists():
                raise ValidationError('Ya existe un elemento con este nombre.')
        return item

    def clean_cantidad_recibida(self):
        cantidad = self.cleaned_data.get('cantidad_recibida')
        if cantidad <= 0:
            raise ValidationError('La cantidad recibida debe ser mayor a 0.')
        return cantidad

    def clean_cantidad_contratada(self):
        cantidad = self.cleaned_data.get('cantidad_contratada')
        if cantidad <= 0:
            raise ValidationError('La cantidad contratada debe ser mayor a 0.')
        return cantidad

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'programa_formacion', 'num_ficha', 'proyecto', 'instructor', 'aprendiz', 
            'num_aprendices', 'num_contrato', 'obs_general', 'fecha_inicio_programa'
        ]
        widgets = {
            'programa_formacion': forms.TextInput(attrs={
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
                'rows': 3,
            }),
            'fecha_inicio_programa': forms.DateInput(attrs={
                'placeholder': 'Fecha de inicio del programa',
                'class': 'form-control',
                'type': 'date',
            }),
        }

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = ['elemento', 'cantidad']
        widgets = {
            'elemento': Select2Widget(attrs={
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Cantidad a registrar',
                'class': 'form-control',
                'min': 1,
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad

class ReporteForm(forms.Form):
    FORMATO_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    formato = forms.ChoiceField(
        choices=FORMATO_CHOICES,
        label='Formato del Reporte',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )
