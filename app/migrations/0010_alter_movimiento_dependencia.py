# Generated by Django 5.1.3 on 2024-11-28 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_elemento_detalle_movimiento_id_elemento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='dependencia',
            field=models.CharField(max_length=200, null=True, verbose_name='Dependencia'),
        ),
    ]