# Generated by Django 3.2.19 on 2023-10-10 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0013_remove_triggeractioncampaign_next_action'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triggeractioncampaign',
            name='is_ready_to_next_action',
        ),
    ]
