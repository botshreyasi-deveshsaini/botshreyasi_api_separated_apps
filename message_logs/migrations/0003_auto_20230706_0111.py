# Generated by Django 3.2.19 on 2023-07-05 19:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('message_logs', '0002_alter_messagelogs_read_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagelogs',
            old_name='candidate_id',
            new_name='candidate',
        ),
        migrations.AddField(
            model_name='messagelogs',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='messagelogs',
            name='is_send',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='messagelogs',
            name='subject',
            field=models.CharField(max_length=500),
        ),
    ]