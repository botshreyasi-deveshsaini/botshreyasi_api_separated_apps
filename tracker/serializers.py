from rest_framework import serializers
from .models import TrackerMaster,Tracker

class TrackerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackerMaster
        fields = '__all__'


class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = '__all__'