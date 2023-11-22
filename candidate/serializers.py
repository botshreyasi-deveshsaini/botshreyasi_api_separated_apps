# serializers.py

from rest_framework import serializers
from .models import CandidateDetails

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateDetails
        fields = '__all__'
