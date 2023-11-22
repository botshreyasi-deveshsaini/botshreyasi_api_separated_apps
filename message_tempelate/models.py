from django.db import models
from application.models import Application
from authorization.models import User
# Create your models here.
class EmailHeaderFooter(models.Model):
    email_header = models.CharField(max_length=200)
    email_footer = models.CharField(max_length=200)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='added_email_header_footer', db_column='added_by')
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'email_headers_footers'

class MessageTemplates(models.Model):
    template_name = models.CharField(max_length=100, blank=False, null=False)
    template_type = models.CharField(db_column='template_type', max_length=50, blank=False, null=False)  # Field name made lowercase.
    template_area = models.CharField(max_length=45, blank=False, null=False)
    subject = models.CharField(max_length=255)
    message = models.TextField(blank=False, null=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='added_message_tempalte', db_column='added_by')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    # email_header_footer = models.ImageField(default=0)#models.ForeignKey(EmailHeaderFooter, on_delete=models.CASCADE, default=None, blank=True, null=True)
    sended_by = models.CharField(db_column='sended_by', default='passive', max_length=50, blank=False, null=False)
    sender_name = models.CharField(db_column='sender_name', default='Bot Shreyasi', max_length=50, blank=False, null=False)
    dlt_te_id = models.CharField(db_column='dtl_te_id', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'message_templates'
