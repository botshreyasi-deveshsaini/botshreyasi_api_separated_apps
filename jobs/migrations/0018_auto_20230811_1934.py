# Generated by Django 3.2.19 on 2023-08-11 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0017_jobunderrecruiters_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobunderrecruiters',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='JUR_job_id', to='jobs.addnewjob'),
        ),
        migrations.AlterField(
            model_name='jobunderrecruiters',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='JUR_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
