# Generated by Django 3.2.19 on 2023-10-23 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_log', '0004_emailslogs_url_shortner'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplates',
            name='design',
            field=models.TextField(blank=True, null=True),
        ),
    ]
