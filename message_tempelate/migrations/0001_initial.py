# Generated by Django 3.2.19 on 2023-07-03 20:19

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
            name='MessageTemplates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('templatename', models.CharField(max_length=100)),
                ('template_type', models.CharField(db_column='templateType', max_length=50)),
                ('template_area', models.CharField(max_length=45)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('dlt_te_id', models.CharField(db_column='dtl_te_id', max_length=100)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(db_column='added_by', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='added_message_tempalte', to=settings.AUTH_USER_MODEL)),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.application')),
            ],
            options={
                'db_table': 'message_templates',
                'managed': True,
            },
        ),
    ]