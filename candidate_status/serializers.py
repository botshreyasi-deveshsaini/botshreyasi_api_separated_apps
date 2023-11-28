
# ----------------

from rest_framework import serializers

from candidate_status.models import CandidateStatus, CandidateStatusRelations
from candidate.models import CandidateDetails

from history.models import History
from jobs.models import AddToJob

class Serializer1(serializers.ModelSerializer):

    class Meta:
        model = CandidateStatus
        fields = '__all__'

class CandidateStatusRelationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateStatusRelations
        fields = '__all__'

class CandidateDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateDetails
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'