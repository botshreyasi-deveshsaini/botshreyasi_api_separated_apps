from django.db import models
from application.models import Application
from authorization.models import User
from jobs.models import AddNewJob
from candidate.models import CandidateDetails
from referer.models import Referrer
# Create your models here.
class MyRefers(models.Model):
    referrer = models.ForeignKey(Referrer, on_delete=models.CASCADE, default=1)
    job = models.ForeignKey(AddNewJob, on_delete=models.CASCADE, default=1)
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    is_action_token = models.BooleanField(default=False)
    is_read  =models.BooleanField(default=False)
    reference_mobile_no = models.CharField(max_length=15)
    reference_email = models.CharField(max_length=100)
    reference_name = models.CharField(max_length=100)
    skill_selected = models.CharField(max_length=255)
    linkdin_url = models.CharField(max_length=100)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'my_refers'
   
