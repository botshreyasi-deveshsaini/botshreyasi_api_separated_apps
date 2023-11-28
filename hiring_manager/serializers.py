from rest_framework import serializers
from .models import HiringManagers


class HiringManagersSerializer(serializers.ModelSerializer):
    # dlt_te_id = serializers.CharField(required=True)
    class Meta:
        model = HiringManagers
        fields= '__all__'
