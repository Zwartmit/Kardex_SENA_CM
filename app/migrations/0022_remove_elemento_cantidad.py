# Generated by Django 5.1.3 on 2024-12-04 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_elemento_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elemento',
            name='cantidad',
        ),
    ]