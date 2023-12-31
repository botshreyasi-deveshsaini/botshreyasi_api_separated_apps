# Generated by Django 3.2.19 on 2023-08-18 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20230811_1303'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidate', '0006_alter_candidatedetails_country_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(max_length=6)),
                ('ip_address', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.application')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate.candidatedetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'candidate_notes',
                'managed': True,
            },
        ),
    ]
