from rest_framework import serializers
from .models import Areas,Permissions,RolePermissions

class AreaRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
#   application = serializers.CharField(write_only=True)

  class Meta:
    model = Areas
    fields = '__all__'
#    fields=['area_name',  'application_id']

class PermissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Permissions
    fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = RolePermissions
    fields = '__all__'   
