# Generated by Django 3.2.19 on 2023-10-23 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_log', '0006_auto_20231023_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailslogs',
            name='to_be_sent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
