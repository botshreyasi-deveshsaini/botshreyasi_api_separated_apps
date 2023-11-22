from django.db import models

# Create your models here.
class HiringManagers(models.Model):
    name = models.CharField(max_length=105, blank=True, null=True)
    email = models.CharField(max_length=205)
    mobile = models.CharField(max_length=455, blank=True, null=True)
    app_id = models.IntegerField(blank=True, null=True)
    recruiter_id = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    department_id = models.IntegerField(blank=True, null=True)
    is_deleted = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'hiring_managers'