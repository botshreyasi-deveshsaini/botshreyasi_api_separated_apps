# Generated by Django 3.2.19 on 2023-08-18 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0008_alter_user_mobile_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='short_name',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
