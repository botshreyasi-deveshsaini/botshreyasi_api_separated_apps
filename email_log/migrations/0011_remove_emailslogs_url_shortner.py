# Generated by Django 3.2.19 on 2023-10-25 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_log', '0010_auto_20231026_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailslogs',
            name='url_shortner',
        ),
    ]
