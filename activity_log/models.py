from django.db import models

from botshreyasi_api.application.models import Application
# from candidate.models import CandidateDetails

# Create your models here.

class ActivityLog(models.Model):

    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=400, null=True)
    is_successful = models.BooleanField(null=True)

    user_agent = models.CharField(max_length=255, null=True)
    ip_address = models.CharField(max_length=45, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)  # <- is useful here?
    attempt_name = models.CharField(max_length=255, null=True)
    # application = models.ForeignKey(Application, on_delete=models.CASCADE)
    # user = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    # otp = models.IntegerField(null=True)
    # url = models.CharField(max_length=100, null=True)
    # number_of_attempts = models.IntegerField(null=True)
    logout_time = models.DateTimeField(null=True)


    class Meta:
        managed = True
        db_table = "activity_log"


# from django.db import models

# class ActivityLogModel(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField(null=True)
#     user_agent = models.CharField(max_length=255)
#     ip_address = models.CharField(max_length=45)
#     created_at = models.DateTimeField(null=True)
#     updated_at = models.DateTimeField(null=True)
#     app_id = models.IntegerField()
#     attempt = models.CharField(max_length=45, null=True) # <--- this was changed
#     logout_time = models.DateTimeField(null=True)
#     otp = models.IntegerField(null=True)
#     password = models.CharField(max_length=45, null=True)

