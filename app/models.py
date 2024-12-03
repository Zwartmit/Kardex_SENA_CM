from django.db import models
from .choices import programas

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
    dependencia = models.CharField(max_length=200, null=True, blank=False, verbose_name='Dependencia')

    def __str__(self):
        return f"Programa de formación: {self.programa_formacion} - Ficha: {self.num_ficha}"

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        db_table = 'Movimiento'

class Elemento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name='elementos', verbose_name='Movimiento asociado')
    item = models.CharField(max_length=100, verbose_name='Ítem')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    cantidad_recibida = models.PositiveIntegerField(verbose_name='Cantidad recibida')
    cantidad_contratada = models.PositiveIntegerField(verbose_name='Cantidad contratada')
    saldo = models.PositiveIntegerField(verbose_name='Saldo pendiente de entrega')
    observaciones = models.CharField(max_length=500, null=True, blank=True, verbose_name='Observaciones')

    def __str__(self):
        return f"{self.movimiento} - {self.item}"

    class Meta:
        verbose_name = "Elemento"
        verbose_name_plural = 'Elementos'
        db_table = 'Elemento'
