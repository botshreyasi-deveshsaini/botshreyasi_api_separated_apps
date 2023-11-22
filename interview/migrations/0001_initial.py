# Generated by Django 3.2.19 on 2023-10-30 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewScheduleCalls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hiring_manager_id', models.IntegerField(blank=True, null=True)),
                ('candidate_id', models.IntegerField()),
                ('call_id', models.IntegerField(blank=True, null=True)),
                ('candidate_name', models.CharField(db_column='candidate_name', max_length=450)),
                ('job', models.IntegerField()),
                ('call_type', models.CharField(max_length=45)),
                ('application', models.IntegerField()),
                ('user', models.IntegerField(blank=True, null=True)),
                ('isinterview_schedule', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=450, null=True)),
                ('plocation', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('call_date_time', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('last_action_time', models.DateTimeField(blank=True, null=True)),
                ('is_inbound', models.IntegerField(blank=True, null=True)),
                ('inter_schedule_for', models.CharField(blank=True, max_length=45, null=True)),
                ('interview_date_time1', models.DateTimeField(blank=True, null=True)),
                ('interview_date_time2', models.DateTimeField(blank=True, null=True)),
                ('interview_date_time3', models.DateTimeField(blank=True, null=True)),
                ('candidate_selected_time', models.DateTimeField(blank=True, null=True)),
                ('candidate_comment', models.TextField(blank=True, null=True)),
                ('candidate_confirm', models.IntegerField(blank=True, null=True)),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('request_new_time', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'interview_schedule_calls',
                'managed': False,
            },
        ),
    ]