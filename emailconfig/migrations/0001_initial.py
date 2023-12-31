# Generated by Django 3.2.19 on 2023-07-05 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('message_logs', '0007_messagelogs_message_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('receiver_type', models.CharField(max_length=20)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('message_log', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='application_Email_tracker', to='message_logs.messagelogs')),
            ],
            options={
                'db_table': 'email_trackers',
                'managed': True,
            },
        ),
    ]
