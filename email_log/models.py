from django.db import models
import uuid
from application.models import Application
from authorization.models import User
from campaign_trigger.models import TriggerActionCampaign,ActionTrigger
from candidate.models import CandidateDetails
# Create your models here.
class EmailTemplates(models.Model):
    template_name = models.CharField(max_length=100, blank=False, null=False)
    # template_type = models.CharField(db_column='template_type', max_length=50, blank=False, null=False)  # Field name made lowercase.
    template_area = models.CharField(max_length=45, blank=False, null=False)
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=False, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='added_email_tempalate', db_column='added_by')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    # email_header_footer = models.ImageField(default=0)#models.ForeignKey(EmailHeaderFooter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    sended_by = models.CharField(db_column='sended_by', default='passive', max_length=50, blank=False, null=False)
    sender_name = models.CharField(db_column='sender_name', default='Bot Shreyasi', max_length=50, blank=False, null=False)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    design = models.TextField(null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'email_templates'

class EmailsLogs(models.Model):
    uid = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    sended_by = models.CharField(db_column='sended_by', default='noreply', max_length=50, blank=False, null=False)
    sended_to = models.EmailField(db_column='sended_to', max_length=50, blank=False, null=False)
    is_send = models.IntegerField(default=0) #models.ForeignKey(MessageStatus, db_column='is_send', on_delete=models.CASCADE, default=0, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True,blank=True)
    message = models.TextField(blank=False, null=False)
    subject = models.CharField(max_length=500, null=True)
    attachment = models.CharField(max_length=500, blank=True,null=True)
    sended_cc = models.CharField(max_length=500, blank=True,null=True)
    sended_bcc = models.CharField(max_length=500, blank=True,null=True)
    sent_date = models.DateTimeField()
    to_be_sent_date = models.DateTimeField(blank=True,null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='added_email_log', db_column='added_by')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1,related_name='application_email_log')
    candidate= models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, default=1)
    email_template= models.ForeignKey(EmailTemplates, on_delete=models.CASCADE, default=3)
    is_otp = models.IntegerField()
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    sender_name = models.CharField(db_column='sender_name', default='Bot Shreyasi', max_length=50, blank=False, null=False)
    is_update = models.IntegerField(blank=True,null=True)
    campaign_trigger_history = models.ForeignKey(TriggerActionCampaign, on_delete=models.SET_NULL, blank=True,null=True)
    campaign_trigger = models.ForeignKey(ActionTrigger, on_delete=models.SET_NULL, blank=True,null=True)

    # ------
    is_smtp = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'email_logs'

