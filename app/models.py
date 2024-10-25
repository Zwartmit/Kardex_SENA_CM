from django.core.exceptions import ValidationError
from django.db import models

class Elemento(models.Model):
    item = models.CharField(max_length=100, unique=True, null=False, blank=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False)

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
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name='movimientos', null=False)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')], null=False, blank=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')

    def __str__(self):
        return f"{self.tipo} - {self.elemento.item} - {self.cantidad}"

    class Meta:
        verbose_name = "movimiento"
        verbose_name_plural = 'movimientos'
        db_table = 'Movimiento'
