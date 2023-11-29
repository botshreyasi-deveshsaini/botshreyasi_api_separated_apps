from django.db import models
from application.models import Application
# from message_tempelate.models import MessageTemplates
from message_log.models import SmsTemplates
from email_log.models import EmailTemplates
# Create your models here.


class RefererPaymentStatus(models.Model):
    status_name = models.CharField(max_length=100, blank=False, null=False)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'referer_payment_statuses'


class CandidateStatus(models.Model):
    display_name = models.CharField(max_length=255, blank=False, null=False)
    root_name = models.CharField(max_length=255, blank=False, null=False)
    is_interview = models.BooleanField(default=False)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    referer_status = models.ForeignKey(RefererPaymentStatus, on_delete=models.CASCADE,
                                       blank=False, null=False, related_name='refer_status', default=1)
    candidate_email_template = models.ForeignKey(
        EmailTemplates, on_delete=models.CASCADE, blank=True, null=True, related_name='candidate_email_template_id')
    candidate_sms_template = models.ForeignKey(
        SmsTemplates, on_delete=models.CASCADE, blank=True, null=True, related_name='candidate_sms_template_id')
    referer_email_template = models.ForeignKey(
        EmailTemplates, on_delete=models.CASCADE, blank=True, null=True, related_name='referer_email_template_id')
    referer_sms_template = models.ForeignKey(
        SmsTemplates, on_delete=models.CASCADE, blank=True, null=True, related_name='referer_sms_template_id')
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'candidate_statuses'


class CandidateStatusRelations(models.Model):
    candidate_status = models.ForeignKey(
        CandidateStatus, on_delete=models.CASCADE, default=1, related_name='candidate_status')
    candidate_status_child = models.ForeignKey(
        CandidateStatus, on_delete=models.CASCADE, default=1, related_name='candidate_status_child')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'candidate_statuses_relations'
