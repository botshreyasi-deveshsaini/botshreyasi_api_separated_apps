# Generated by Django 3.2.19 on 2023-08-22 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0007_rename_refer_status_candidatestatus_referer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatestatus',
            name='referer_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='refer_status', to='candidate_status.refererpaymentstatus'),
        ),
    ]