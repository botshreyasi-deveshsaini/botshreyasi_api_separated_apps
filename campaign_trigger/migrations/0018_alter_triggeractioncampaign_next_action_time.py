# Generated by Django 3.2.19 on 2023-10-11 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0017_rename_candidate_status_triggeractioncampaign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triggeractioncampaign',
            name='next_action_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
