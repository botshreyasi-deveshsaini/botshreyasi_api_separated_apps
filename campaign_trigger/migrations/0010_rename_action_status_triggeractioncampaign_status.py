# Generated by Django 3.2.19 on 2023-10-09 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0009_triggeractioncampaign_channel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='triggeractioncampaign',
            old_name='action_status',
            new_name='status',
        ),
    ]