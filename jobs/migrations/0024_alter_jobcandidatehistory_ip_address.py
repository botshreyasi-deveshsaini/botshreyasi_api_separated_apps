# Generated by Django 3.2.19 on 2023-08-22 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0023_alter_jobcandidatehistory_reminder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcandidatehistory',
            name='ip_address',
            field=models.CharField(blank=True, default='0.0.0.0', max_length=150, null=True),
        ),
    ]