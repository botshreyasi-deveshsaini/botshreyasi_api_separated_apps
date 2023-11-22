from django.db import models
from application.models import Application
from authorization.models import User
from candidate.models import CandidateDetails
from message_logs.models import MessageLogs
import uuid
import random
import string
from campaign_trigger.models import TriggerActionCampaign,ActionTrigger
from campaign.models import Campaign
from email_log.models import EmailsLogs
from message_log.models import SMSLogs
# Create your models here.
def generate_random_uid():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

class UrlShortners(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    candidate= models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, default=1)
    url_name =  models.CharField(max_length=45,blank=False,null=False)
    old_url = models.CharField(max_length=100,blank=False,null=False)
    url_key = models.CharField(max_length=12, default=generate_random_uid, unique=True)
    link_invalid = models.BooleanField(default=False)
    url_opened = models.BooleanField(default=False)
    url_opened_time = models.DateTimeField(null=True)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    chat_key = models.CharField(max_length=100, blank=True,null=True)
    campaign_trigger_history = models.ForeignKey(TriggerActionCampaign, on_delete=models.SET_NULL, blank=True, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, blank=True, null=True)
    email_log = models.ForeignKey(EmailsLogs, on_delete=models.SET_NULL, blank=True, null=True)
    sms_log = models.ForeignKey(SMSLogs, on_delete=models.SET_NULL, blank=True, null=True)

    url_for = models.CharField(max_length=45, null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'url_shortners'
