# Generated by Django 3.2.19 on 2023-08-22 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0006_auto_20230822_1319'),
        ('jobs', '0019_addtojob_is_referred'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtojob',
            name='referer_payment_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='candidate_status.refererpaymentstatus'),
        ),
    ]
