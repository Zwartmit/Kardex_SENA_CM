# Generated by Django 5.1.3 on 2024-12-04 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_elemento_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elemento',
            name='cantidad_contratada',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='cantidad_recibida',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='movimiento',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='observaciones',
        ),
        migrations.RemoveField(
            model_name='elemento',
            name='saldo',
        ),
        migrations.CreateModel(
            name='DetalleMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_recibida', models.PositiveIntegerField(default=0, verbose_name='Cantidad recibida')),
                ('cantidad_contratada', models.PositiveIntegerField(default=0, verbose_name='Cantidad contratada')),
                ('saldo', models.PositiveIntegerField(default=0, verbose_name='Saldo pendiente de entrega')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('elemento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.elemento', verbose_name='Elemento')),
                ('movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='app.movimiento', verbose_name='Movimiento')),
            ],
            options={
                'verbose_name': 'Detalle de Movimiento',
                'verbose_name_plural': 'Detalles de Movimientos',
                'db_table': 'DetalleMovimiento',
            },
        ),
    ]