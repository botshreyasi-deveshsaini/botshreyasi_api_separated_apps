# Generated by Django 3.2.19 on 2023-08-21 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0003_auto_20230821_1914'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RefererPaymentStatus',
        ),
    ]
