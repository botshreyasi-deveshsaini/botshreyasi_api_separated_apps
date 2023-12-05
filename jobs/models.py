from django.db import models
from authorization.models import User
from application.models import Application
from departments.models import Department
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime
from candidate.models import CandidateDetails
from referer.models import Referrer
from candidate_status.models import CandidateStatus, RefererPaymentStatus
from campaign.models import Campaign, CampaignEvent
# Create your models here.


class AddNewJob(models.Model):
    experience_regex = RegexValidator(
        regex=r'^\d{1,2}(\.\d{1,2})?$',
        message='Experience must be in format: 0-99 or 0.0-99.99'
    )
    salary_regex = RegexValidator(
        regex=r'^\d{1,3}(,\d{3})*(\.\d{1,2})?$',
        message='Salary must be in format: 0-999,999.99'
    )
    creater = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='created_jobs')
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='managed_jobs')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, default=1)
    slug = models.CharField(max_length=100, default='')
    job_title = models.CharField(max_length=100)
    job_status = models.CharField(max_length=100, default='Active')
    job_description = models.TextField()
    minimum_experience = models.IntegerField(validators=[experience_regex])
    maximum_experience = models.IntegerField(validators=[experience_regex])
    minimum_salary = models.IntegerField()
    maximum_salary = models.IntegerField()
    number_of_opening = models.IntegerField()
    is_referral = models.BooleanField(default=False)
    referral_bonus = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    is_visible_on_app = models.BooleanField(default=False)
    visible_start_date = models.DateTimeField(null=True, blank=True)
    visible_end_date = models.DateTimeField(null=True, blank=True)
    keyskills = models.CharField(
        blank=False, null=False, max_length=255, default='')
    first_skill = models.CharField(
        blank=False, null=False, max_length=150, default='')
    second_skill = models.CharField(
        blank=False, null=False, max_length=150, default='')
    third_skill = models.CharField(
        blank=False, null=False, max_length=150, default='')
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    hiring_manager_id =  models.TextField(blank=True,null=True)
    event_name =  models.TextField(blank=True,null=True)
    min_rating =  models.IntegerField(default=0)
    interview_round = models.IntegerField(default=0)
    interview_within = models.IntegerField(default=0)
    auto_Integration = models.CharField(max_length=45,default='No')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.job_title)
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'job_details'

    def clean(self):
        if self.is_referral and self.referral_bonus is None:
            raise ValueError(
                "Referral bonus is required when isReferral is set to 'Yes'.")
        if self.is_visible_on_app and (self.visible_start_date is None or self.visible_end_date is None):
            raise models.ValidationError(
                "Both startdate and enddate are required when is_visible_on_app is set to 'Yes'.")
        if self.maximum_experience is not None and self.minimum_experience is not None:
            if float(self.maximum_experience) <= float(self.minimum_experience):
                raise ValidationError(
                    "Maximum experience must be greater than minimum experience.")


class FunctionalAreas(models.Model):
    functional_areas_name = models.CharField(
        max_length=100, null=False, blank=False)
    code = models.CharField(max_length=8, null=False, blank=False)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'functional_areas'


class Industries(models.Model):
    industry_name = models.CharField(max_length=100, null=False, blank=False)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'industries'


class InternationalLocations(models.Model):
    location = models.CharField(max_length=100, null=False, blank=False)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'job_international_locations'


class Location(models.Model):
    location = models.CharField(max_length=100, null=False, blank=False)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'job_locations'


class JobUnderRecruiters(models.Model):
    job = models.ForeignKey(
        AddNewJob, on_delete=models.CASCADE, default=1, related_name='JUR_job_id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='JUR_user_id')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    assign_start = models.DateTimeField(blank=True, null=True)
    assign_end = models.DateTimeField(blank=True, null=True)
    is_unassigned = models.BooleanField()
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'job_under_recruiters'


class AddToJob(models.Model):
    candidate = models.ForeignKey(
        CandidateDetails, on_delete=models.CASCADE, default=1, related_name='candidate_id')
    job = models.ForeignKey(
        AddNewJob, on_delete=models.CASCADE, default=1, related_name='job_id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='recruiter_id')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(
        CandidateStatus, on_delete=models.CASCADE, default=1)
    referer_status = models.ForeignKey(
        RefererPaymentStatus, on_delete=models.CASCADE, default=1)
    referrer = models.ForeignKey(
        Referrer, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_referred = models.BooleanField(default=False)
    # attachmentsFolder = models.CharField(max_length=1000, null=True)
    attachment = models.CharField(max_length=1000, null=True)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, default=1)
    campaign_event = models.ForeignKey(
        CampaignEvent, on_delete=models.CASCADE, default=1)
    campaign_status = models.IntegerField(default=0)
    campaign_run_time = models.DateTimeField(default=datetime.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'add_to_jobs'


class JobTag(models.Model):
    job = models.ForeignKey(
        AddNewJob, on_delete=models.CASCADE, default=1, related_name='tag_job_id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='tag_recruiter_id')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'job_tags'


class JobCandidateHistory(models.Model):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE,
                                  default=1, related_name='JobCandidateHistory_candidate_id')
    atj = models.ForeignKey(AddToJob, on_delete=models.CASCADE,
                            default=1, related_name='JobCandidateHistory_atj_id')
    job = models.ForeignKey(AddNewJob, on_delete=models.CASCADE,
                            default=1, related_name='JobCandidateHistory_job_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             default=1, related_name='JobCandidateHistory_recruiter_id')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(
        CandidateStatus, on_delete=models.CASCADE, default=1)
    comment = models.TextField(blank=True, null=True)
    attachment = models.CharField(max_length=1000, null=True)
    is_interview = models.BooleanField(default=False)
    reminder_date = models.DateField(blank=True, null=True)
    ip_address = models.CharField(
        max_length=150, default='0.0.0.0', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'job_candidate_histories'
