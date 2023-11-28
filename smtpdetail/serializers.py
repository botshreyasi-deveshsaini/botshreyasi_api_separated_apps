# from email.mime import application
# from rest_framework import serializers
# from .models import *



# class SMTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=SMTPDetails
#         fields='__all__'

from rest_framework import serializers

from .models import EmailData

class EmailDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailData
        fields = "__all__"
