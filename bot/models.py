from django.db import models
from application.models import Application
from authorization.models import User
# Create your models here.

def get_default_custom_data():
    return {'joblocation': '[joblocation]', 'jobtitle': '[jobtitle]', 'first_name': '[first_name]'}

class BotDetails(models.Model):
    bot_name =  models.CharField(db_column='bot_name', blank=False,null=False,max_length=45)
    description= models.TextField(db_column='bot_description', blank=False,null=False,max_length=1550)
    category=models.CharField(blank=False,null=False,max_length=150)
    is_published=models.BooleanField(default=False)
    custom_data= models.JSONField(blank=False,null=False,default=get_default_custom_data)
    application=models.ForeignKey(Application, on_delete=models.CASCADE)
    created_by=models.ForeignKey(User,db_column='created_by', on_delete=models.CASCADE)
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    file_name = models.CharField(max_length=45, default='bot23')
    class Meta:
        managed = True
        db_table = 'bot_details'