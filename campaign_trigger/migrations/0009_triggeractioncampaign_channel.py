# Generated by Django 3.2.19 on 2023-10-08 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0010_campaignchannel_channel_root_name'),
        ('campaign_trigger', '0008_alter_triggeractioncampaign_next_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggeractioncampaign',
            name='channel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='campaign.campaignchannel'),
        ),
    ]
