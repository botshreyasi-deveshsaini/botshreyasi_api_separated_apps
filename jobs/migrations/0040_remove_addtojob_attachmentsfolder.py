# Generated by Django 3.2.19 on 2023-12-05 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0039_auto_20231205_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addtojob',
            name='attachmentsFolder',
        ),
    ]