# Generated by Django 3.2.19 on 2023-06-28 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_tracker_trackermaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trackermaster',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]