from rest_framework import serializers
from jobs.models import AddNewJob,Location,InternationalLocations,AddToJob


class AddNewJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddNewJob
        fields= "__all__"
        
class InternationalLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalLocations
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
class AddToJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToJob
        fields= "__all__"
        