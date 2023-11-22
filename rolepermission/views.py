from multiprocessing import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from helper.views import *
from .renderers import AreaRenderer
from .serializers import AreaRegistrationSerializer,PermissionSerializer,RolePermissionSerializer
from .models import Areas
from rest_framework import status

# @method_decorator(csrf_exempt, name='dispatch')
class getPermission(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        User = getUser()
        roleid = User['role_id']
        permission = GetQueryData(f'SELECT p.slug from permissions p where p.id in(select rp.permission_id from role_permissions rp where rp.role_id={roleid})')
        return Response(permission)

    
      

@method_decorator(csrf_exempt, name='dispatch')
class AreaRegistrationView(APIView):
  permission_classes = (IsAuthenticated,)
  renderer_classes = [AreaRenderer]
  def post(self, request, format=None):
    print("............................................")
    data = request.data.copy()
    application =GetAppID()
    data['application'] = application
    serializer = AreaRegistrationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Areas Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)
 
class AreaUpdateView(APIView):
  permission_classes = (IsAuthenticated,)
  renderer_classes = [AreaRenderer]  
  def post( request, *args, **kwargs):
    print("---------------------")
    print(args)
    print("....................")
    user = Areas.objects.get(id=area_id)
    serializer = AreaRegistrationSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  



class PermissionView(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self, request, format=None):
    print(f"Permission Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {request.data}")
    serializer = PermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Permission Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)
 


class RolePermissionView(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self, request, format=None):
    print(f"Role Permission Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {request.data}")
    serializer = RolePermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Role Permission Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)
