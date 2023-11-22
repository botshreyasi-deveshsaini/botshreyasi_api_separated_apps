# Generated by Django 3.2.19 on 2023-09-01 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '0004_auto_20230811_1303'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidate', '0007_candidatenotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=100)),
                ('template_type', models.CharField(db_column='template_type', max_length=50)),
                ('template_area', models.CharField(max_length=45)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('sended_by', models.CharField(db_column='sended_by', default='passive', max_length=50)),
                ('sender_name', models.CharField(db_column='sender_name', default='Bot Shreyasi', max_length=50)),
                ('dlt_te_id', models.CharField(blank=True, db_column='dtl_te_id', max_length=100, null=True)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(db_column='added_by', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='added_email_tempalate', to=settings.AUTH_USER_MODEL)),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.application')),
            ],
            options={
                'db_table': 'email_templates',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EmailsLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default=uuid.uuid4, max_length=200, unique=True)),
                ('sended_by', models.CharField(db_column='sended_by', default='noreply', max_length=50)),
                ('sended_to', models.EmailField(db_column='sended_to', max_length=50)),
                ('is_send', models.IntegerField(default=0)),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(default='')),
                ('message', models.TextField()),
                ('subject', models.CharField(max_length=500)),
                ('attachment', models.CharField(max_length=500)),
                ('sended_cc', models.CharField(max_length=500)),
                ('sended_bcc', models.CharField(max_length=500)),
                ('sent_date', models.DateTimeField()),
                ('to_be_sent_date', models.DateTimeField()),
                ('is_otp', models.IntegerField()),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(db_column='added_by', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='added_email_log', to=settings.AUTH_USER_MODEL)),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='application_email_log', to='application.application')),
                ('candidate', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='candidate.candidatedetails')),
                ('email_template', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='email_log.emailtemplates')),
            ],
            options={
                'db_table': 'email_logs',
                'managed': True,
            },
        ),
    ]