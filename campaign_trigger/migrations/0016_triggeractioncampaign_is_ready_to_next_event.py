# Generated by Django 3.2.19 on 2023-10-11 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0015_rename_status_triggeractioncampaign_candidate_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='is_ready_to_next_event',
            field=models.BooleanField(default=False),
        ),
    ]
