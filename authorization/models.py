
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from datetime import datetime, timedelta
from botshreyasi_api.application.models import Application
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, username, name, application,first_name,last_name, password=None, password2=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            application=application,
            first_name = first_name,
            last_name=last_name,
            **extra_fields
        )
        # user.
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name,  last_name, phone, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_admin = True
        user.is_staff = True
        user.name = f'{first_name} {last_name}'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    mobile_no_regex = RegexValidator(
        regex=r'^\d{3,15}$',
        message="Mobile number must be between 3 and 15 digits."
    )
    # id=models.AutoField(primary_key=True,null=False)
    uid = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    role_id = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=False, max_length=100, unique=True)
    first_name = models.CharField(null=False, max_length=100)
    last_name = models.CharField(null=False, max_length=100, default='.')
    username = models.CharField(null=False, max_length=100)
    phone = models.CharField(null=True, unique=True,max_length=12)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(null=False, max_length=100)
    gender = models.IntegerField(null=True)
    profile_pic = models.CharField(null=True, blank=True, max_length=150)
    mobile_no = models.CharField(
        max_length=150, null=False, unique=True, default='1',validators=[mobile_no_regex],)
    dob = models.DateField(default='2022-08-12')
    # app_id = models.IntegerField(blank=False, null=False, default=0)
    # application = models.ForeignKey(Application, on_delete=models.CASCADE)
    application_id = models.IntegerField(default=1)
    manager = models.IntegerField(blank=True, null=True)
    short_name = models.CharField(null=False, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    login_attempts = models.IntegerField(default=0)
    forget_password_attempts = models.IntegerField(default=0)
    account_locked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'mobile_no', 'name']
    password = models.CharField(max_length=1024)

    objects = UserManager()

    def __str__(self):
        return self.email + ", " + self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        managed = True
        db_table = 'users'