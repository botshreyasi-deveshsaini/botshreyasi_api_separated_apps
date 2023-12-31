# Generated by Django 3.2.19 on 2023-11-24 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    # replaces = [('hiring_manager', '0001_initial'), ('hiring_manager', '0002_alter_hiringmanagers_email'), ('hiring_manager', '0003_alter_hiringmanagers_email')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HiringManagers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_id', models.IntegerField(blank=True, null=True)),
                ('available_end_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('available_start_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('calendar', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('department_id', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(max_length=205, null=True)),
                ('is_deleted', models.CharField(default=False, max_length=10)),
                ('mobile', models.CharField(blank=True, max_length=455, null=True)),
                ('msg_send', models.CharField(default='', max_length=500)),
                ('name', models.CharField(blank=True, max_length=105, null=True)),
                ('off_day', models.DateField(null=True)),
                ('platform', models.CharField(max_length=100, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'hiring_managers',
                'managed': True,
            },
        ),
    ]
