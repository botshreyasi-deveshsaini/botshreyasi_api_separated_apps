from ipaddress import ip_address
from django.db import models
from authorization.models import User
from candidate.models import CandidateDetails
from application.models import Application

class Source(models.Model):
    source_name=models.CharField(max_length=55, blank=False,null=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        managed = True
        db_table = 'Sources'

class History(models.Model):
    candidate = models.ForeignKey(CandidateDetails, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    source=models.ForeignKey(Source, on_delete=models.CASCADE, default=1)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'histories'


