# Generated by Django 3.2.19 on 2023-10-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='botdetails',
            name='file_name',
            field=models.CharField(default='bot23', max_length=45),
        ),
    ]
