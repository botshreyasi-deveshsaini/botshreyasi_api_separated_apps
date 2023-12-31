# Generated by Django 3.2.19 on 2023-08-11 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_remove_application_appname_mail_sms'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationDefault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_status_id', models.IntegerField(default=1)),
                ('default_referrer_status_id', models.IntegerField(default=2)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.application')),
            ],
        ),
    ]
