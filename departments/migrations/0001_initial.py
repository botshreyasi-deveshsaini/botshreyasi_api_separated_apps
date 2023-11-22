# Generated by Django 3.2.19 on 2023-06-23 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_or_department', models.CharField(default='department', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='application.application')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('head_of_department', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='head_of_department', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'application_departments',
                'managed': True,
            },
        ),
    ]