from django.db import models
from django.forms import ValidationError
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
        return f"Entregado al aprendiz {self.aprendiz} de la ficha {self.num_ficha} ({self.programa_formacion})"

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        db_table = 'Movimiento'

class Elemento(models.Model):
    descripcion = models.CharField(null=True, blank=False, max_length=200, verbose_name='Descripción')

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name = "Elemento"
        verbose_name_plural = 'Elementos'
        db_table = 'Elemento'

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name='detalles',)
    elemento = models.ForeignKey(Elemento, on_delete=models.PROTECT, verbose_name="Elemento")
    cantidad_recibida = models.PositiveIntegerField(null=True, blank=False, verbose_name="Cantidad recibida")
    cantidad_contratada = models.PositiveIntegerField(null=True, blank=False, verbose_name="Cantidad contratada")
    saldo = models.PositiveIntegerField(null=True, blank=False, verbose_name="Saldo pendiente de entrega")
    observaciones = models.TextField(null=True, blank=False, verbose_name="Observaciones")

    def clean(self):
            super().clean()
            if not self.cantidad_recibida and not self.cantidad_contratada:
                raise ValidationError({
                    'cantidad_recibida': 'Debe especificar al menos una cantidad recibida o contratada.',
                    'cantidad_contratada': 'Debe especificar al menos una cantidad recibida o contratada.',
                })

    def __str__(self):
        
        return f"Detalle de {self.movimiento} - {self.elemento}"

    class Meta:
        verbose_name = "Detalle de Movimiento"
        verbose_name_plural = "Detalles de Movimientos"
        db_table = "DetalleMovimiento"