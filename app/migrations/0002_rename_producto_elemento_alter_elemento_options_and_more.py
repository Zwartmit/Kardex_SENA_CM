# Generated by Django 5.1.2 on 2024-10-25 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Producto',
            new_name='Elemento',
        ),
        migrations.AlterModelOptions(
            name='elemento',
            options={'verbose_name': 'elemento', 'verbose_name_plural': 'elementos'},
        ),
        migrations.RenameField(
            model_name='movimiento',
            old_name='producto',
            new_name='elemento',
        ),
        migrations.AlterModelTable(
            name='elemento',
            table='Elemento',
        ),
    ]
