# Generated by Django 3.2.19 on 2023-08-22 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0006_auto_20230822_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidatestatus',
            old_name='refer_status',
            new_name='referer_status',
        ),
    ]
