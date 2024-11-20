from django import forms
from .choices import programas
from django.core.exceptions import ValidationError
from django.db import models

class Elemento(models.Model):
    item = models.CharField(max_length=100, unique=True, null=True, blank=False, verbose_name='Elemento')
    cantidad_recibida = models.PositiveIntegerField(null=True, blank=False, verbose_name='Cantidad recibida')
    cantidad_contratada = models.PositiveIntegerField(null=True, blank=False, verbose_name='Cantidad contratada')
    unidad_medida = models.CharField(max_length=100, null=True, blank=False, verbose_name='Unidad de medida')
    observaciones = models.CharField(max_length=500, null=True, blank=False, verbose_name='Observaciones')

    def __str__(self):
        return f"Elemento: {self.item} - Cantidad recibida: {self.cantidad_recibida} - Cantidad contratada: {self.cantidad_contratada} - Unidad de medida: {self.unidad_medida} - Observaciones: {self.observaciones}"
    
    class Meta:
        verbose_name = "elemento"
        verbose_name_plural = 'elementos'
        db_table = 'Elemento'

class Movimiento(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    programa_formacion = models.CharField(max_length=100, choices=[(prog, prog) for prog in programas], null=True, blank=False, verbose_name='Programa de formación')
    num_ficha = models.PositiveIntegerField(null=True, blank=False, verbose_name='Ficha')
    proyecto = models.CharField(max_length=200, null=True, blank=False, verbose_name='Proyecto')
    instructor = models.CharField(max_length=200, null=True, blank=False, verbose_name='Instructor')
    aprendiz = models.CharField(max_length=200, null=True, blank=False, verbose_name='Aprendiz')
    num_aprendices = models.PositiveIntegerField(null=True, blank=False, verbose_name='Número de aprendices')
    num_contrato = models.PositiveIntegerField(null=True, blank=False, verbose_name='Contrato')
    obs_general = models.CharField(max_length=500, null=True, blank=False, verbose_name='Observaciones generales')
    fecha_inicio_programa = models.DateField(null=True, blank=False, verbose_name='Fecha de inicio del programa de formación')

    def __str__(self):
        return f"Ficha: {self.num_ficha} - Proyecto: {self.proyecto} - Fecha: {self.fecha}"

    class Meta:
        verbose_name = "movimiento"
        verbose_name_plural = 'movimientos'
        db_table = 'Movimiento'

class Detalle_movimiento(models.Model):
    elemento = models.ForeignKey(Elemento, null=True, blank=False, on_delete=models.CASCADE, related_name='detalles', verbose_name='Elemento')
    movimiento = models.ForeignKey(Movimiento, null=True, blank=False, on_delete=models.CASCADE, related_name='detalles', verbose_name='Movimiento')
    
    def __str__(self):
        return f"Elemento: {self.elemento.item} - Cantidad recibida: {self.elemento.cantidad_recibida} - Cantidad contratada: {self.elemento.cantidad_contratada} -  Movimiento: {self.movimiento}"

    class Meta:
        verbose_name = "detalle_movimiento"
        verbose_name_plural = 'detalles_movimiento'
        db_table = 'DetalleMovimiento'
