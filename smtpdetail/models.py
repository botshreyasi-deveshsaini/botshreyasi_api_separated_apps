from django.db import models
from application.models import Application
from authorization.models import User

class SMTPDetails(models.Model):
    smtp_type = models.CharField(max_length=15)
    smtp_name = models.CharField(max_length=15, null=False,blank=False)
    user_name = models.CharField(max_length=15, null=False,blank=False)
    password = models.CharField(max_length=15, null=False,blank=False)
    port = models.IntegerField(null=False,blank=False)
    ssl_enabled = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    # ------
    is_smtp = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'smtp_details'



# from django.db import models
# from django.core.validators import validate_email
# from smtpdetail.validators import validate_domain_name, validate_username, validate_hostname, validate_port


# # Create your models here.

# # ----- Move to separate file ---- #
# # ---------- Validators ---------- #

# # def domainNameValidator(value):
# #     domain_name_regex = r"[a-z]+\.[a-z]+"
# #     validate_url = RegexValidator(regex=domain_name_regex)

# #     return validate_url(value)


# class EmailData(models.Model):
#     senderEmail = models.CharField(max_length=255, blank=True, null=False, validators=[validate_email])

#     # validators can be used to enforce strong passwords too
#     password = models.CharField(max_length=255, blank=True, null=False)

#     username = models.CharField(max_length=255, blank=True, null=False, validators=[validate_username])
#     domainName = models.CharField(max_length=255, blank=True, null=False, validators=[validate_domain_name])

#     smtpHost = models.CharField(max_length=255, blank=True, null=True, validators=[validate_hostname])
#     smtpPort = models.IntegerField(blank=True, null=True, validators=[validate_port])

#     toEmail = models.CharField(max_length=255, blank=True, null=False, validators=[validate_email])
#     message = models.CharField(max_length=1023, blank=True, null=False)  # length arbitrary, change later

#     def save(self, *args, **kwargs):

#         if self.senderEmail:
#             self.username, self.domainName = self.senderEmail.split("@")

#         elif self.username and self.domainName:
#             self.senderEmail = "@".join([self.username, self.domainName])

#         super().save(*args, **kwargs)



#     # def validate(self):
#         # super().validate()

#         # EmailValidator(self.email)

#     @staticmethod
#     def test(a):
#         return a

#     class Meta:
#         managed = True
#         db_table = "email_data"
#         # unique_together = ['senderEmail', 'smtpHost', 'smtpPort']


