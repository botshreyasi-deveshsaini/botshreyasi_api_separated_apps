# Generated by Django 3.2.19 on 2023-11-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiring_manager', '0006_alter_hiringmanagers_off_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiringmanagers',
            name='is_deleted',
            field=models.BooleanField(default=False, max_length=10),
        ),
    ]