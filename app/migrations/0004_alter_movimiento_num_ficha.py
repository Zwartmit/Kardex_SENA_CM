# Generated by Django 5.1.2 on 2024-10-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_elemento_cantidad_alter_elemento_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='num_ficha',
            field=models.PositiveIntegerField(null=True, verbose_name='Ficha'),
        ),
    ]