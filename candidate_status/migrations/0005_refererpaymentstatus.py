# Generated by Django 3.2.19 on 2023-08-21 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_status', '0004_delete_refererpaymentstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefererPaymentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=100)),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'referer_payment_statuses',
                'managed': True,
            },
        ),
    ]