from typing_extensions import Required
from rest_framework import serializers
from .models import SmsTemplates,SMSLogs


class SmsTemplates_serializer(serializers.ModelSerializer):
    # dlt_te_id = serializers.CharField(required=True)
    class Meta:
        model = SmsTemplates
        fields= '__all__'

class SmsLogs_serializer(serializers.ModelSerializer):
    # dlt_te_id = serializers.CharField(required=True)
    class Meta:
        model = SMSLogs
        fields= '__all__'