# Generated by Django 3.2.19 on 2023-10-25 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0024_alter_triggeractioncampaign_action_temp_id'),
        ('message_log', '0010_smslogs_is_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smslogs',
            name='url_shortner',
        ),
        migrations.AddField(
            model_name='smslogs',
            name='campaign_trigger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_trigger.actiontrigger'),
        ),
        migrations.AddField(
            model_name='smslogs',
            name='campaign_trigger_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_trigger.triggeractioncampaign'),
        ),
    ]
