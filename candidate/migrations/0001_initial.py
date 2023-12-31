# Generated by Django 3.2.19 on 2023-06-20 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=45, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=45, null=True)),
                ('last_name', models.CharField(blank=True, max_length=45, null=True)),
                ('full_name', models.CharField(blank=True, max_length=191, null=True)),
                ('mobile_no', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('pan_no', models.CharField(blank=True, max_length=6, null=True)),
                ('aadharcard_number', models.IntegerField(blank=True, null=True)),
                ('skill_set', models.CharField(blank=True, max_length=445, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('current_organization', models.CharField(blank=True, max_length=90, null=True)),
                ('current_designation', models.CharField(blank=True, max_length=90, null=True)),
                ('ovarall_experiance', models.CharField(blank=True, max_length=90, null=True)),
                ('relevant_experiance', models.CharField(blank=True, max_length=90, null=True)),
                ('qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('preferred_location', models.CharField(blank=True, max_length=190, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('current_salary', models.CharField(blank=True, max_length=100, null=True)),
                ('expected_salary', models.CharField(blank=True, max_length=100, null=True)),
                ('notice_period', models.IntegerField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('industry_type', models.CharField(blank=True, max_length=100, null=True)),
                ('functional_area', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('resume', models.CharField(blank=True, max_length=100, null=True)),
                ('cvhtml', models.TextField(blank=True, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=100, null=True)),
                ('jobboard_url', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.application')),
            ],
            options={
                'db_table': 'candidate_details',
                'managed': True,
                'unique_together': {('application', 'email')},
            },
        ),
    ]
