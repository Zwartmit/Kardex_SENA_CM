from django import forms
from django.core.exceptions import ValidationError
from django.db import models

class Elemento(models.Model):
    item = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name='Elemento')
    cantidad = models.PositiveIntegerField(null=False, blank=False, verbose_name='Cantidad')

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')

    def __str__(self):
        return self.item
    
    class Meta:
        verbose_name = "elemento"
        verbose_name_plural = 'elementos'
        db_table = 'Elemento'

class Movimiento(models.Model):
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name='movimientos', null=False, blank=False, verbose_name='Elemento')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    num_ficha = models.PositiveIntegerField(null=True, blank=False, verbose_name='Ficha')
    cantidad = models.PositiveIntegerField(null=False, blank=False, verbose_name='Cantidad')
    proyecto = models.CharField(max_length=200, default='', null=False, blank=False, verbose_name='Proyecto')
    descripcion = models.CharField(max_length=500, default='', null=False, blank=False, verbose_name='Descripción')

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')
        
    def clean_num_ficha(self):
            num_ficha = self.cleaned_data.get('num_ficha')
            if num_ficha == '':
                raise forms.ValidationError('Este campo es obligatorio y no puede estar vacío.')
            return num_ficha
    
    def __str__(self):
        return (f"Movimiento: {self.tipo} - "
                f"Elemento: {self.elemento.item} - "
                f"Cantidad: {self.cantidad} - "
                f"Ficha: {self.num_ficha} - "
                f"Proyecto: {self.proyecto} - "
                f"Descripción: {self.descripcion} - "
                f"Fecha: {self.fecha}")

    class Meta:
        verbose_name = "movimiento"
        verbose_name_plural = 'movimientos'
        db_table = 'Movimiento'
