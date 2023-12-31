# Generated by Django 3.2.19 on 2023-07-21 20:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_candidatedetails_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatedetails',
            name='country_code',
            field=models.CharField(default='+91', max_length=4, validators=[django.core.validators.RegexValidator(message="Country code must be in the format '+123'.", regex='^\\+\\d{1,3}$')]),
        ),
    ]
