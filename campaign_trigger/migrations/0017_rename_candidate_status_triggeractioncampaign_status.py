# Generated by Django 3.2.19 on 2023-10-11 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0016_triggeractioncampaign_is_ready_to_next_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='triggeractioncampaign',
            old_name='candidate_status',
            new_name='status',
        ),
    ]
