from django.shortcuts import render
from rest_framework.views import APIView
from helper.views import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import BotSerializer
# Create your views here.


class BotListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Datas>>>>>>>>>>>>>>>>---->{request.data}")
        application_id = GetAppID()
        user_id = GetUserID()
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        mutable_data['created_by'] = user_id
        serializer = BotSerializer(data=mutable_data)
        try:
            if serializer.is_valid():
                bot = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        application_id = GetAppID()
        user_id = GetUserID()
        child_roles = GetChildWithSelf(application_id, user_id)
        if not child_roles:
            child_roles = f"[{user_id}]"
        child_roles = ','.join(map(str, child_roles))
        params = [application_id, user_id, child_roles]
        data = GetStoreProcedureData(
            'GetBotDetails', params)
        return Response(data)
