# Generated by Django 3.2.19 on 2023-09-10 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_log', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smstemplates',
            name='template_type',
        ),
    ]
