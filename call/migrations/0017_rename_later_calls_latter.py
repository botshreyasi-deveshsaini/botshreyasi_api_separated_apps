# Generated by Django 3.2.19 on 2023-10-14 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('call', '0016_auto_20231014_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calls',
            old_name='later',
            new_name='latter',
        ),
    ]