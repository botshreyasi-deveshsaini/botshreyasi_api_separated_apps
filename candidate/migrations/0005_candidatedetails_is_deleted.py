# Generated by Django 3.2.19 on 2023-07-19 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0004_auto_20230713_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatedetails',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
