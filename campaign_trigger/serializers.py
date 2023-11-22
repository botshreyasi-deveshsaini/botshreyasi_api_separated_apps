from rest_framework import serializers
from .models import TriggerActionCampaign, ActionTrigger


class TriggerActionCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggerActionCampaign
        fields = '__all__'


class ActionTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionTrigger
        fields = '__all__'