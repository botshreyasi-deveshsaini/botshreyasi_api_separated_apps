# Generated by Django 3.2.19 on 2023-10-09 04:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0010_rename_action_status_triggeractioncampaign_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='action_run_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='is_ready_to_next_action',
            field=models.BooleanField(default=False),
        ),
    ]