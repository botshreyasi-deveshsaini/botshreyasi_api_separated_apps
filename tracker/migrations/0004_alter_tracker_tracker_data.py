# Generated by Django 3.2.19 on 2023-06-28 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20230629_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='tracker_data',
            field=models.JSONField(),
        ),
    ]
