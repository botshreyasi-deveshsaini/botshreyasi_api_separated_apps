# Generated by Django 3.2.19 on 2023-09-10 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_log', '0003_alter_smstemplates_dlt_te_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smstemplates',
            name='dlt_te_id',
        ),
    ]
