# Generated by Django 3.2.19 on 2023-09-10 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_log', '0002_remove_smstemplates_template_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smstemplates',
            name='dlt_te_id',
            field=models.CharField(db_column='dtl_te_id', max_length=100, null=True),
        ),
    ]
