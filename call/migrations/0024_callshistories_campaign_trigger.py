# Generated by Django 3.2.19 on 2023-10-31 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0024_alter_triggeractioncampaign_action_temp_id'),
        ('call', '0023_auto_20231101_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='callshistories',
            name='campaign_trigger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_trigger.actiontrigger'),
        ),
    ]