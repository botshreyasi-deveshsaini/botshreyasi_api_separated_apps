from django.db import models
from application.models import Application
from authorization.models import User

# Create your models here.


class SmsTemplates(models.Model):
    template_name = models.CharField(max_length=100, blank=False, null=False)
    template_area = models.CharField(max_length=45, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1,
                                 related_name='added_sms_tempalate', db_column='added_by')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, default=1)
    sended_by = models.CharField(
        db_column='sended_by', default='passive', max_length=50, blank=False, null=False)
    sender_name = models.CharField(
        db_column='sender_name', default='Bot Shreyasi', max_length=50, blank=False, null=False)
    # Field name made lowercase.
    dlt_te_id = models.CharField(
        db_column='dlt_te_id', max_length=100, blank=False, null=True)
    ip_address = models.CharField(
        blank=False, null=False, max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'sms_templates'