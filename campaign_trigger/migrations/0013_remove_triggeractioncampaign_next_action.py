# Generated by Django 3.2.19 on 2023-10-10 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0012_auto_20231010_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triggeractioncampaign',
            name='next_action',
        ),
    ]
