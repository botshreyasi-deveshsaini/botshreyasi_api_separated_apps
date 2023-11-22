from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from application.models import Application
from authorization.models import User
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class Uploads(models.Model):
    # image = models.ImageField(upload_to="images")
    image = models.FileField(upload_to='images')

class Tracker(models.Model):
    tracker_name  = models.CharField(max_length=45, blank=False, null=False, unique=True)
    tracker_data = models.JSONField()
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_by =  models.ForeignKey(User,on_delete=models.CASCADE)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'trackers'

class TrackerMaster(models.Model): 
    display_name  = models.CharField(max_length=45, blank=False, null=False,)
    db_name = models.CharField(max_length=45, blank=False, null=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_by =  models.ForeignKey(User,on_delete=models.CASCADE)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_job_specific = models.BooleanField(default=False) 
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'tracker_masters'
# Create your models here.
