from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from application.models import Application
from authorization.models import User
from .templates_models import SmsTemplates
from candidate.models import CandidateDetails
# Create your models here.

class SMSLogs(models.Model):
    mobile_no_validator = RegexValidator(
        regex=r'^\d{4,11}$',  # Example: 4 to 11 digits
        message="mobile_no number must be between 4 and 11 digits."
    )
    uid = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    sended_by = models.CharField(
        db_column='sended_by', default='noreply', max_length=50, blank=False, null=False)
    sended_to = models.CharField(db_column='sended_to', max_length=50,
                                 blank=False, null=False, validators=[mobile_no_validator])
    # models.ForeignKey(MessageStatus, db_column='is_send', on_delete=models.CASCADE, default=0, blank=True, null=True)
    is_send = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    message = models.TextField(blank=False, null=False)
    sent_date = models.DateTimeField()
    to_be_sent_date = models.DateTimeField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                 default=1, related_name='added_sms_log', db_column='added_by')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1, related_name='application_sms_log')
    candidate = models.ForeignKey(
        CandidateDetails, on_delete=models.CASCADE, default=1)
    sms_template = models.ForeignKey(
        SmsTemplates, on_delete=models.CASCADE, default=3)
    is_otp = models.IntegerField()
    # Field name made lowercase.
    dlt_te_id = models.CharField(
        db_column='dtl_te_id', max_length=100, blank=False, null=True)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_update = models.IntegerField(blank=True,null=True)
    # campaign_trigger_history = models.ForeignKey(TriggerActionCampaign, on_delete=models.SET_NULL, blank=True,null=True)
    # campaign_trigger = models.ForeignKey(ActionTrigger, on_delete=models.SET_NULL, blank=True,null=True)
    
    class Meta:
        managed = True
        db_table = 'sms_logs'
