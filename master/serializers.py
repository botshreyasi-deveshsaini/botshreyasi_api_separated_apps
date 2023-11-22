from rest_framework import serializers
from jobs.models import Industries,FunctionalAreas

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = '__all__'

class FunctionalAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionalAreas
        fields = '__all__'
