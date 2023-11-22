# Generated by Django 3.2.19 on 2023-07-12 19:00

import bot.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BotDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_name', models.CharField(db_column='bot_name', max_length=45)),
                ('description', models.TextField(db_column='bot_description', max_length=1550)),
                ('category', models.CharField(max_length=150)),
                ('is_published', models.BooleanField(default=False)),
                ('custom_data', models.JSONField(default=bot.models.get_default_custom_data)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.application')),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bot_details',
                'managed': True,
            },
        ),
    ]