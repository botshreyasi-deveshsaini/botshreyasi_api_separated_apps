# Generated by Django 3.2.19 on 2023-10-25 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0024_alter_triggeractioncampaign_action_temp_id'),
        ('email_log', '0009_emailslogs_is_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailslogs',
            name='campaign_trigger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_trigger.actiontrigger'),
        ),
        migrations.AddField(
            model_name='emailslogs',
            name='campaign_trigger_history',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_trigger.triggeractioncampaign'),
        ),
    ]
