from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from helper.views import *
from rest_framework.permissions import IsAuthenticated
from .serializers import SmsTemplates_serializer, SmsLogs_serializer
from .models import SmsTemplates


class SmsTemplatesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = int(request.GET.get('id', 0))

        application_id = GetAppID()
        user_id = GetUserID()
        child_roles = GetChildWithSelf(application_id, user_id)
        if not child_roles:
            child_roles = f"[{user_id}]"
        child_roles = ','.join(map(str, child_roles))
        params = [application_id, user_id, child_roles, id]
        data = GetStoreProcedureData(
            'GetSmsTemplates', params)
        return Response(data)

    def post(self, request):
        # try:
        data = request.data
        print("manoj:::::::::::::::::::::::::::::::::::::::::::")
        mutable_data = request.data.copy()
        mutable_data['application'] = GetAppID()
        mutable_data['added_by'] = GetUserID()
        Messagetempelate_email = SmsTemplates_serializer(data=mutable_data)
        if Messagetempelate_email.is_valid(raise_exception=True):
            Job = Messagetempelate_email.save()
            return Response(Messagetempelate_email.data, status=status.HTTP_201_CREATED)
        return Response(Messagetempelate_email.errors, status=status.HTTP_400_BAD_REQUEST)

        # except as e:
        # return Response("THIS IS NOT CORRECT WAY TO REQUEST")
    def put(self, request, id):
        try:
            Sms_Templates = SmsTemplates.objects.get(id=id)
        except Sms_Templates.DoesNotExist:
            return Response({'error': 'Templates not found'}, status=status.HTTP_404_NOT_FOUND)

        application_id = GetAppID()
        added_by = GetUserID()
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        mutable_data['added_by'] = added_by

        serializer = SmsTemplates_serializer(Sms_Templates, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            sms_tmplates = SmsTemplates.objects.get(id=id)
        except sms_tmplates.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        sms_tmplates.is_deleted = True
        sms_tmplates.save()
        return Response({'status': 'deleted'})


class StoreInMessageLog():
    def SendSMS(data):
        print(f"data-------> {data}")
        MessageteLog = SmsLogs_serializer(data=data)
        if MessageteLog.is_valid(raise_exception=True):
            Log = MessageteLog.save()
            return Response(MessageteLog.data, status=status.HTTP_201_CREATED)
        return Response(MessageteLog.errors, status=status.HTTP_400_BAD_REQUEST)
