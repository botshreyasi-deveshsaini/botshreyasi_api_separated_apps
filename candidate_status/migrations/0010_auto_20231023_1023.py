# Generated by Django 3.2.19 on 2023-10-23 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0009_auto_20230911_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatestatus',
            name='candidate_email_template',
        ),
        migrations.RemoveField(
            model_name='candidatestatus',
            name='candidate_sms_template',
        ),
        migrations.RemoveField(
            model_name='candidatestatus',
            name='referer_email_template',
        ),
        migrations.RemoveField(
            model_name='candidatestatus',
            name='referer_sms_template',
        ),
    ]
