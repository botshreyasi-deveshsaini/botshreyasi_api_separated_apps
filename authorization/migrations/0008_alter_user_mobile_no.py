# Generated by Django 3.2.19 on 2023-06-28 08:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0007_alter_user_mobile_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_no',
            field=models.CharField(default='1', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Mobile number must be between 3 and 15 digits.', regex='^\\d{3,15}$')]),
        ),
    ]
