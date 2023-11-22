# serializers.py

from rest_framework import serializers
from .models import BotDetails

class BotSerializer(serializers.ModelSerializer):

    class Meta:
        model = BotDetails
        fields = '__all__'
