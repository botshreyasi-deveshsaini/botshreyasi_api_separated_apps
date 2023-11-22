# serializers.py

from rest_framework import serializers
from .models import Campaign, CampaignEvent


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignEvent
        fields = '__all__'
        

    def create(self, validated_data):
        return CampaignEvent.objects.create(**validated_data)
    
class CampaignEventSerializerCall(serializers.Serializer):  # Use Serializer instead of ModelSerializer
    id = serializers.IntegerField()
    name = serializers.CharField(source='event_name')  # Map event_name to name

    class Meta:
        fields = ('id', 'name')