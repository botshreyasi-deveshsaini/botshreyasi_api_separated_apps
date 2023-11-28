# Generated by Django 3.2.19 on 2023-11-27 09:54

import django.core.validators
from django.db import migrations, models
import hiring_manager.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiring_manager', '0004_alter_hiringmanagers_off_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hiringmanagers',
            name='off_day',
        ),
        migrations.AddField(
            model_name='hiringmanagers',
            name='off_days',
            field=models.BigIntegerField(null=True, validators=[hiring_manager.validators.OffDaysValidator()]),
        ),
        migrations.AlterField(
            model_name='hiringmanagers',
            name='email',
            field=models.CharField(max_length=205, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='hiringmanagers',
            name='mobile',
            field=models.CharField(blank=True, max_length=455, null=True, validators=[hiring_manager.validators.IndianMobileNumberValidator()]),
        ),
    ]