# Generated by Django 3.2.19 on 2023-11-30 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity_log', '0002_activitylog_updated_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActivityLog',
        ),
    ]