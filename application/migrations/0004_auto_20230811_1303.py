# Generated by Django 3.2.19 on 2023-08-11 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_applicationdefault'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationdefault',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='applicationdefault',
            table='application_defaults',
        ),
    ]
