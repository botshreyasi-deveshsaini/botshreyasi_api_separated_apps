# Generated by Django 3.2.19 on 2023-10-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0010_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=1024),
        ),
    ]
