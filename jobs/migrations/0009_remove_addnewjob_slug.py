# Generated by Django 3.2.19 on 2023-06-30 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_addnewjob_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addnewjob',
            name='slug',
        ),
    ]