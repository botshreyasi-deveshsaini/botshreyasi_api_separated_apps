# Generated by Django 3.2.19 on 2023-10-23 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortner', '0005_auto_20231022_2045'),
        ('email_log', '0003_remove_emailtemplates_template_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailslogs',
            name='url_shortner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='url_shortner.urlshortners'),
        ),
    ]