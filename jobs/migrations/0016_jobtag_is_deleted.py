# Generated by Django 3.2.19 on 2023-08-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0015_addnewjob_job_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtag',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]