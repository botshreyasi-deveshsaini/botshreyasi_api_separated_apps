# Generated by Django 3.2.19 on 2023-06-26 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_auto_20230626_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]