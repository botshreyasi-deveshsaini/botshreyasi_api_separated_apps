from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.core.validators import RegexValidator

# Create your models here.
class Referrer(AbstractBaseUser):
    mobile_no_regex = RegexValidator(
        regex=r'^\d{3,15}$',
        message="Mobile number must be between 3 and 15 digits."
    )
    # id=models.AutoField(primary_key=True,null=False)
    uid = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    is_email_confirmed =models.BooleanField(default=False) 
    is_mobile_confirmed =models.BooleanField(default=False) 
    is_internal_referrer = models.BooleanField(default=False)
    email = models.EmailField(null=False, max_length=100, unique=True)
    first_name = models.CharField(null=False, max_length=100)
    last_name = models.CharField(null=False, max_length=100, default='.')
    username = models.CharField(null=False, max_length=100)
    phone = models.CharField(null=True, unique=True,max_length=12)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(null=False, max_length=100)
    gender = models.IntegerField(null=True)
    profile_pic = models.CharField(null=True, blank=True, max_length=150)
    mobile_no = models.CharField(
        max_length=150, null=False, unique=True, default='1',validators=[mobile_no_regex],)
    dob = models.DateField(default='2022-08-12')

    # app_id = models.IntegerField(blank=False, null=False, default=0)
    # application = models.ForeignKey(Application, on_delete=models.CASCADE)
    # manager = models.IntegerField(blank=True, null=True)
    short_name = models.CharField(null=False, max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'mobile_no', 'name']

    # objects = UserManager()

    def __str__(self):
        return self.email + ", " + self.first_name

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        managed = True
        db_table = 'referrers'
        

