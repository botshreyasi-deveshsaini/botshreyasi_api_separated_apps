# Generated by Django 3.2.19 on 2023-07-19 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_name', models.CharField(max_length=255, unique=True)),
                ('application_address', models.TextField()),
                ('is_ats', models.IntegerField()),
                ('application_mobileno', models.CharField(max_length=100)),
                ('license_start_date', models.DateField(auto_now_add=True)),
                ('license_end_date', models.DateField()),
                ('no_of_license', models.IntegerField(default=1)),
                ('website', models.CharField(max_length=255)),
                ('application_pan_no', models.CharField(max_length=150)),
                ('application_gst_no', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('default_status_id', models.IntegerField()),
                ('default_referrer_id', models.IntegerField()),
                ('secret_key', models.CharField(max_length=255)),
                ('term_and_condition', models.BooleanField(default=False)),
                ('state_name', models.CharField(max_length=150)),
                ('logo_url', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('can_call', models.BooleanField(default=False)),
                ('disable_crowed_sourcing', models.BooleanField(default=False)),
                ('application_about', models.TextField()),
                ('call_port_allow', models.IntegerField(default=2)),
                ('working_days', models.IntegerField(default=5)),
                ('billing_name', models.CharField(max_length=150)),
                ('appname_mail_sms', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'applications',
                'managed': True,
            },
        ),
    ]
