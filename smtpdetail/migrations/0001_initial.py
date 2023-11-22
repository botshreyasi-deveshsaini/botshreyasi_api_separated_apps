# Generated by Django 3.2.15 on 2022-08-16 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMTPDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_type', models.CharField(max_length=15)),
                ('smtp_name', models.CharField(max_length=15)),
                ('user_name', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=15)),
                ('port', models.IntegerField()),
                ('ssl_enabled', models.BooleanField(default=False)),
                ('app_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'smtp_details',
                'managed': True,
            },
        ),
    ]
