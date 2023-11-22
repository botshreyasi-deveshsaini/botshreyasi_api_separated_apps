from django.db import models
from authorization.models import User
from application.models import Application
from candidate_status.models import CandidateStatus
# from email_log.models import EmailTemplates
# from message_log.models import SmsTemplates
# from bot.models  import BotDetails
# Create your models here.


class Campaign(models.Model):
    is_published = models.BooleanField(default=False)
    campaign_name = models.CharField(blank=False, null=False, max_length=255)
    campaign_description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1,)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'campaigns'


class CampaignChannel(models.Model):
    channel_name = models.CharField(blank=False, null=False, max_length=45)
    channel_root_name = models.CharField(
        blank=False, null=False, max_length=45, default=channel_name)

    class Meta:
        managed = True
        db_table = 'campaign_channels'


class CampaignEvent(models.Model):
    is_published = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, default=1)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)
    event_name = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=True, null=True)
    candidate_status = models.ForeignKey(
        CandidateStatus, on_delete=models.SET_NULL, blank=True, null=True)
    event_type = models.CharField(blank=False, null=False, max_length=25)
    event_order = models.IntegerField()
    trigger_date = models.DateTimeField(blank=True, null=True)
    trigger_interval = models.IntegerField(blank=True, null=True)
    trigger_interval_unit = models.CharField(
        blank=True, null=True, max_length=25)
    trigger_mode = models.CharField(blank=True, null=True, max_length=45)
    channel = models.CharField(blank=True, null=True, max_length=45)
    channel = models.ForeignKey(
        CampaignChannel, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1,)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    color = models.CharField(blank=False, null=False,max_length=25, default='#388E3C')
    temp_id = models.IntegerField(blank=True, null=True)
    flow_type = models.CharField(blank=True, null=True, max_length=45)
    flow_up_id = models.IntegerField(blank=True, null=True)
    sms_template_id =   models.IntegerField(blank=True, null=True)
    email_template_id = models.IntegerField(blank=True, null=True)
    bot_id =            models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'campaign_events'

