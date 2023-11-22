from django.shortcuts import render
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializer import DepartmentSerializer
from helper.views import *
# Create your views here.
class DepartmentListCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print("-----------------")
        application_id = GetAppID()
        isclientdepartment  = request.GET.get('isclientdepartment')
        application_departments = Department.objects.filter(application_id=application_id,client_or_department=isclientdepartment, is_deleted=False).values()
        print(application_departments)
        return Response(application_departments)
    
    def post(self, request):
        queryset = Department.objects.all()
        application_id = GetAppID()
        user_id = GetUserID()
        ip_address = request.META.get('REMOTE_ADDR')
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        mutable_data['created_by'] = user_id
        mutable_data['ip_address'] = ip_address
        print(ip_address)
        serializer = DepartmentSerializer(data=mutable_data)
        if serializer.is_valid():
            department = serializer.save()
            print(mutable_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BED_REQUEST)



class DepartmentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(is_deleted=instance.is_deleted)

class ClientListCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print("-----------------")
        application_id = GetAppID()
        isclientdepartment  = 'Client'
        application_departments = Department.objects.filter(application_id=application_id,client_or_department=isclientdepartment, is_deleted=False).values()
        print(application_departments)
        return Response(application_departments)
    
    def post(self, request):
        application_id = GetAppID()
        user_id = GetUserID()
        ip_address = request.META.get('REMOTE_ADDR')
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        mutable_data['created_by'] = user_id
        mutable_data['ip_address'] = ip_address
        print(ip_address)
        serializer = DepartmentSerializer(data=mutable_data)
        if serializer.is_valid():
            department = serializer.save()
            print(mutable_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BED_REQUEST)

class ClientListCreateViewSingle(APIView):
    def patch(self, request, id):
        print("-----------------")
        application_id = GetAppID()
        isclientdepartment  = 'Client'
        application_departments = Department.objects.get(id) #filter(application_id=application_id,client_or_department=isclientdepartment,id is_deleted=False).values()
        print(application_departments)
        return Response(application_departments)
    