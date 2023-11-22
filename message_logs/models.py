from django.db import models
from application.models import Application
from authorization.models import User
from candidate.models import CandidateDetails
from message_tempelate.models import MessageTemplates
import uuid

# Create your models here.

class MessageStatus(models.Model):
    status_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'message_status'

class MessageLogs(models.Model):
    uid = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    message_type = models.CharField(db_column='message_type', max_length=50, blank=False, null=False)
    sended_by = models.CharField(db_column='sended_by', default='noreply', max_length=50, blank=False, null=False)
    sended_to = models.EmailField(db_column='sended_to', max_length=50, blank=False, null=False)
    is_send = models.IntegerField(default=0) #models.ForeignKey(MessageStatus, db_column='is_send', on_delete=models.CASCADE, default=0, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(default='')
    message = models.TextField(blank=False, null=False)
    subject = models.CharField(max_length=500)
    attachment = models.CharField(max_length=500)
    sended_cc = models.CharField(max_length=500)
    sended_bcc = models.CharField(max_length=500)
    sent_date = models.DateTimeField()
    to_be_sent_date = models.DateTimeField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='added_message_log', db_column='added_by')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1,related_name='application_message_log')
    candidate= models.ForeignKey(CandidateDetails, on_delete=models.CASCADE, default=1)
    message_template= models.ForeignKey(MessageTemplates, on_delete=models.CASCADE, default=3)
    is_otp = models.IntegerField()
    dlt_te_id = models.CharField(db_column='dtl_te_id', max_length=100, blank=False, null=False)  # Field name made lowercase.
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'message_logs'


class MessageUnsubscribers(models.Model):
    email = models.EmailField(max_length=50)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'email_unsubscribers'