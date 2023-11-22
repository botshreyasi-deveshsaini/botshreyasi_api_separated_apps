from typing_extensions import Required
from rest_framework import serializers
from .models import EmailTemplates,EmailsLogs


class EmailTemplates_serializer(serializers.ModelSerializer):
    # dlt_te_id = serializers.CharField(required=True)
    class Meta:
        model = EmailTemplates
        fields= '__all__'

class EmailLogs_serializer(serializers.ModelSerializer):
    # dlt_te_id = serializers.CharField(required=True)
    class Meta:
        model = EmailsLogs
        fields= '__all__'