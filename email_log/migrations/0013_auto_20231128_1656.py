# Generated by Django 3.2.19 on 2023-11-28 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_log', '0012_emailslogs_is_smtp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailslogs',
            name='campaign_trigger',
        ),
        migrations.RemoveField(
            model_name='emailslogs',
            name='campaign_trigger_history',
        ),
    ]
