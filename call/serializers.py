# serializers.py

from rest_framework import serializers
from .models import Calls, CallsHistories

class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calls
        fields = '__all__'


class CallsHistoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallsHistories
        fields = '__all__'