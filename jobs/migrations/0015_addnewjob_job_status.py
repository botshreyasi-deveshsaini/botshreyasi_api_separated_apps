# Generated by Django 3.2.19 on 2023-08-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_jobtag'),
    ]

    operations = [
        migrations.AddField(
            model_name='addnewjob',
            name='job_status',
            field=models.CharField(default='Active', max_length=100),
        ),
    ]
