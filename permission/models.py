# models.py
from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100)
    areas = models.ManyToManyField(Area)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

# class User(AbstractUser):
#     user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.username

class RolePermission(models.Model):
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_role.name} - {self.permission.name}"
