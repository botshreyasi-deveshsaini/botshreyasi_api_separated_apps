# Generated by Django 3.2.19 on 2023-10-30 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20231026_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='is_update',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
