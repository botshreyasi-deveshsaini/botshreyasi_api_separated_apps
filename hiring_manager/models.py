from django.db import models
from .validators import validate_email, validate_indian_mobile, validate_off_days

from application.models import Application
from candidate.models import CandidateDetails
from departments.models import Department


# Create your models here.
class HiringManagers(models.Model):
    name = models.CharField(max_length=105, blank=True, null=True)
    # email = models.CharField(max_length=205)
    email = models.CharField(max_length=205, null=True, validators=[validate_email])
    mobile = models.CharField(max_length=455, blank=True, null=True, validators=[validate_indian_mobile])
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(max_length=10, default=False)

    available_start_time = models.TimeField(null=True)
    available_end_time = models.TimeField(null=True)
    # off_days = models.CharField(max_length=100, null=True, validators=[validate_off_days])
    off_days = models.CharField(max_length=100, null=True)

    msg_send = models.CharField(max_length=500, default="")
    platform = models.CharField(max_length=100, null=True)
    calendar = models.CharField(max_length=100, null=True)

    class Meta:
        managed = True
        db_table = 'hiring_managers'
        unique_together = ("email", "mobile", "application_id")
