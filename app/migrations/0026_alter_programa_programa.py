# Generated by Django 5.1.6 on 2025-03-03 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_programa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programa',
            name='programa',
            field=models.CharField(max_length=200, null=True, verbose_name='Descripción'),
        ),
    ]
