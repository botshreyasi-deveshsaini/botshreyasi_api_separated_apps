# Generated by Django 3.2.19 on 2023-09-03 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0026_auto_20230903_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtojob',
            name='campaign_run_time',
            field=models.DateTimeField(default='2023-09-04 02:25:00'),
        ),
    ]