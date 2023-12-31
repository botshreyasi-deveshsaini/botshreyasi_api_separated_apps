# Generated by Django 3.2.19 on 2023-10-06 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('candidate', '0007_candidatenotes'),
        ('jobs', '0035_addtojob_campaign_run_time'),
        ('candidate_status', '0009_auto_20230911_1659'),
        ('campaign', '0010_campaignchannel_channel_root_name'),
        ('application', '0004_auto_20230811_1303'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign_trigger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerActionCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_name', models.CharField(max_length=45)),
                ('action_root_name', models.CharField(max_length=45)),
                ('action_temp_id', models.IntegerField(default=1)),
                ('next_action_time', models.DateTimeField(blank=True)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action_status', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate_status.candidatestatus')),
                ('add_to_job', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobs.addtojob')),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.application')),
                ('campaign', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='campaign.campaign')),
                ('candidate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='candidate.candidatedetails')),
                ('event', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='campaign.campaignevent')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'campaign_triggers',
                'managed': True,
            },
        ),
    ]
