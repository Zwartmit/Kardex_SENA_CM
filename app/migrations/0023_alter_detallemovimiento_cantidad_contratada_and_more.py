# Generated by Django 5.1.4 on 2024-12-10 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_elemento_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallemovimiento',
            name='cantidad_contratada',
            field=models.PositiveIntegerField(default=1, verbose_name='Cantidad contratada'),
        ),
        migrations.AlterField(
            model_name='detallemovimiento',
            name='cantidad_recibida',
            field=models.PositiveIntegerField(default=1, verbose_name='Cantidad recibida'),
        ),
    ]