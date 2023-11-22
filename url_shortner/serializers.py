from rest_framework import serializers
from .models import UrlShortners


class UrlShortnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShortners
        fields = '__all__'
