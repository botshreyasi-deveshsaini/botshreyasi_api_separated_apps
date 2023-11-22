from django.db import models

# Create your models here.
class Gender(models.Model):
    gender_name = models.CharField(max_length=45, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'genders'