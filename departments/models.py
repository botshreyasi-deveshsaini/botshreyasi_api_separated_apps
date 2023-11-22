from django.db import models
from authorization.models import User
from application.models import Application
# Create your models here.

class Department(models.Model):
    CLIENT_OR_DEPARTMENT_CHOICES = (
        ('client', 'Client'),
        ('department', 'Department'),
    )
    # client_or_department = models.CharField(max_length=20,default='department')
    client_or_department = models.CharField(
        max_length=20, choices=CLIENT_OR_DEPARTMENT_CHOICES, default='department'
    )
    department_name = models.CharField(max_length=100,null=False,blank=False)
    department_location = models.CharField(max_length=255,null=True,blank=True)
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, related_name='head_of_department', null=True, blank=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='created_by')
    application = models.ForeignKey(Application, on_delete=models.CASCADE,related_name='application')
    ip_address=models.CharField(blank=False,null=False,max_length=150, default='0.0.0.0')
    client_about = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()
        
    def save(self, *args, **kwargs):
        if self.client_or_department == 'client':
            self.head_of_department = None  # Set head_of_department to null when client_or_department is 'client'
        super().save(*args, **kwargs)
    # def __str__(self):
    #     return self.name        
    class Meta:
        managed = True
        db_table = 'application_departments'