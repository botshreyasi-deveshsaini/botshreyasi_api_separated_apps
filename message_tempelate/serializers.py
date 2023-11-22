from typing_extensions import Required
from rest_framework import serializers
from .models import *


class Messagetemplate_sms_serializer(serializers.ModelSerializer):
    dlt_te_id = serializers.CharField(required=True)
    class Meta:
        model = MessageTemplates
        fields= '__all__'

class Messagetemplate_email_serializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplates
        fields= '__all__'