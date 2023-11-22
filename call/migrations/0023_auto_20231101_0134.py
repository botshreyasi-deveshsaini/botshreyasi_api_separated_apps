# Generated by Django 3.2.19 on 2023-10-31 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call', '0022_calls_call_history_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='callshistories',
            name='interview_round',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='callshistories',
            name='status_changed',
            field=models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='callshistories',
            name='submit_to_pannel',
            field=models.IntegerField(default=0),
        ),
    ]
