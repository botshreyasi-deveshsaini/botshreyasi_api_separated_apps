# Generated by Django 3.2.19 on 2023-10-24 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_log', '0008_emailslogs_sender_name'),
        ('emailconfig', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailtracker',
            name='message_log',
        ),
        migrations.AddField(
            model_name='emailtracker',
            name='email_log',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='application_Email_tracker', to='email_log.emailslogs'),
        ),
    ]
