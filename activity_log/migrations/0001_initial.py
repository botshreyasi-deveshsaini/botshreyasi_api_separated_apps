# Generated by Django 3.2.19 on 2023-11-30 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200, null=True)),
                ('password', models.CharField(max_length=400, null=True)),
                ('is_successful', models.BooleanField(null=True)),
                ('user_agent', models.CharField(max_length=255, null=True)),
                ('ip_address', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('otp', models.IntegerField(null=True)),
                ('number_of_attempts', models.IntegerField(null=True)),
                ('logout_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'activity_log',
                'managed': True,
            },
        ),
    ]
