from email.mime import application
from rest_framework import serializers
from .models import *



class SMTPSerializer(serializers.ModelSerializer):
    class Meta:
        model=SMTPDetails
        fields='__all__'