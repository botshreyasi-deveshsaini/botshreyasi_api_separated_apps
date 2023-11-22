from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from helper.views import *
from jobs.models import Industries,FunctionalAreas
from .serializers import IndustrySerializer,FunctionalAreasSerializer

# Create your views here.
class getGender(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        print("????????????????????????????s")
        gender = GetQueryData('select * from genders')
        # permissionqueary = f'select * from genders'
        # print(permissionqueary)
        # permissioncursor = connections["mysqlslave"].cursor()
        # permissioncursor.execute(permissionqueary)
        # permissionRow = permissioncursor.fetchall()
        # permissionColumn = [column[0]
        #     for column in permissioncursor.description]
        # permission = []
        # for event in permissionRow:
        #     permission.append(dict(zip(permissionColumn, event)))
        return Response(gender)
    

class IndustryCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Industries.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)   
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FunctionalAreaCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = FunctionalAreas.objects.all()
    serializer_class = FunctionalAreasSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
     
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
