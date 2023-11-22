# Generated by Django 3.2.19 on 2023-08-25 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0008_alter_candidatestatus_referer_status'),
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaignevent',
            old_name='campaign_id',
            new_name='campaign',
        ),
        migrations.RenameField(
            model_name='campaignevent',
            old_name='parent_id',
            new_name='parent',
        ),
        migrations.RemoveField(
            model_name='campaignevent',
            name='channel_id',
        ),
        migrations.AddField(
            model_name='campaignevent',
            name='candidate_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate_status.candidatestatus'),
        ),
        migrations.AddField(
            model_name='campaignevent',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='channel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='campaign.campaignchannel'),
        ),
    ]