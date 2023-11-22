from rest_framework import serializers
from .models import EmailTracker

class EmailTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTracker
        fields= "__all__"