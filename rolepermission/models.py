# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from application.models import Application
from django.utils.text import slugify


class Areas(models.Model):
    area_name = models.CharField(max_length=255, blank=False, null=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'areas'





class Permissions(models.Model):
    areas = models.ForeignKey(Areas, on_delete=models.CASCADE)
    permission = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(unique=False, max_length=255, blank=True, null=True)
    permission_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(db_column='ip_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'permissions'
        unique_together = ('slug', 'areas_id')

    def save(self, *args, **kwargs):
        # Generate a slug from the title when saving the object
        self.slug = slugify(self.permission_name)
        self.clean()
        super().save(*args, **kwargs)    

class UserRoles(models.Model):
    rolename = models.CharField(db_column='roleName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    can_redistribute_power = models.CharField(max_length=255, blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    update_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(db_column='ip_address', max_length=45, blank=True, null=True)  # Field name made lowercase.
    role_category = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_roles'

class RolePermissions(models.Model):
    role = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=255, blank=True, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    ip_address = models.CharField(db_column='ip_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'role_permissions'
        unique_together = ('role', 'permission')

    # def save(self, *args, **kwargs):
    #     # Fetch the title based on the ID
    #     if self.permission:
    #         title = Permissions.objects.get(id=self.permission)
    #         self.title_name = title.slug
    #     super().save(*args, **kwargs)    



