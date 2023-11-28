from django.db import models
from .validators import validate_email, validate_indian_mobile, validate_off_days

# Create your models here.
class HiringManagers(models.Model):
    name = models.CharField(max_length=105, blank=True, null=True)
    # email = models.CharField(max_length=205)
    email = models.CharField(max_length=205, null=True, validators=[validate_email])
    mobile = models.CharField(max_length=455, blank=True, null=True, validators=[validate_indian_mobile])
    application_id = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(max_length=10, default=False)

    available_start_time = models.DateTimeField(auto_now_add=True, null=True)
    available_end_time = models.DateTimeField(auto_now_add=True, null=True)
    off_days = models.CharField(max_length=100, null=True, validators=[validate_off_days])
    # off_days = models.CharField(max_length=100, null=True)

    msg_send = models.CharField(max_length=500, default="")
    platform = models.CharField(max_length=100, null=True)
    calendar = models.CharField(max_length=100, null=True)

    class Meta:
        managed = True
        db_table = 'hiring_managers'
