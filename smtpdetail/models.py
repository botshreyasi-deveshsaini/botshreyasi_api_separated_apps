from django.db import models
from application.models import Application
from authorization.models import User

class SMTPDetails(models.Model):
    smtp_type = models.CharField(max_length=15)
    smtp_name = models.CharField(max_length=15, null=False,blank=False)
    user_name = models.CharField(max_length=15, null=False,blank=False)
    password = models.CharField(max_length=15, null=False,blank=False)
    port = models.IntegerField(null=False,blank=False)
    ssl_enabled = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'smtp_details'
