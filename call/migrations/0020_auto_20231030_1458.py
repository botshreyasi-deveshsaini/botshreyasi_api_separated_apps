# Generated by Django 3.2.19 on 2023-10-30 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0013_auto_20231023_1703'),
        ('call', '0019_auto_20231024_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='calls',
            name='campaign_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign.campaignevent'),
        ),
        migrations.AddField(
            model_name='calls',
            name='campaing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaign.campaign'),
        ),
    ]
