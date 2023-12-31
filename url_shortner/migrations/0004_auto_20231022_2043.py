# Generated by Django 3.2.19 on 2023-10-22 15:13

from django.db import migrations, models
import url_shortner.models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortner', '0003_remove_urlshortners_message_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlshortners',
            name='url_key',
            field=models.CharField(default=url_shortner.models.generate_random_uid, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='urlshortners',
            name='url_opened_time',
            field=models.DateTimeField(null=True),
        ),
    ]
