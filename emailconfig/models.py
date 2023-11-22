from django.db import models
from email_log.models import  EmailsLogs
# Create your models here.
class EmailTracker(models.Model):
    email= models.EmailField( max_length=50, blank=False, null=False)
    email_log= models.ForeignKey(EmailsLogs, on_delete=models.CASCADE, default=1,related_name='application_Email_tracker')
    receiver_type = models.CharField(max_length=20, blank=False,null=False)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'email_trackers'