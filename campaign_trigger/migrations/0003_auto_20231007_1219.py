# Generated by Django 3.2.19 on 2023-10-07 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_trigger', '0002_triggeractioncampaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='is_action',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='is_next_action',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign_trigger.triggeractioncampaign'),
        ),
    ]
