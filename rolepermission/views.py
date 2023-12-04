from multiprocessing import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from helper.views import *
from .renderers import AreaRenderer
from .serializers import AreaRegistrationSerializer, PermissionSerializer, RolePermissionSerializer, UserRolesSerializer
from .models import Areas, Permissions, RolePermissions, UserRoles
from rest_framework import status


def stringValidator(_str):

  # if 1 <= len(_str) <= 100:
  #   pass

  # for i in string.punctuation + string.digits:
  #   if i in _str:
  #     return False

  # 1 - 100 characters string is allowed (arbitrary: change if necessary)
  reExp = r"^[a-zA-Z][a-zA-Z\-0-9 ]{1,100}$"

  if re.match(reExp, _str):
    return True
  else:
    return False

# @method_decorator(csrf_exempt, name='dispatch')
class getPermission(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        User = getUser()
        roleid = User['role_id']
        permission = GetQueryData(f'SELECT p.slug from permissions p where p.id in(select rp.permission_id from role_permissions rp where rp.role_id={roleid})')
        return Response(permission)

    
      

# @method_decorator(csrf_exempt, name='dispatch')
# class AreaRegistrationView(APIView):
#   permission_classes = (IsAuthenticated,)
#   renderer_classes = [AreaRenderer]
#   def post(self, request, format=None):
#     print("............................................")
#     data = request.data.copy()
#     application =GetAppID()
#     data['application'] = application
#     serializer = AreaRegistrationSerializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     area = serializer.save()
#     return Response({'msg':'Areas Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)
 
# class AreaUpdateView(APIView):
#   permission_classes = (IsAuthenticated,)
#   renderer_classes = [AreaRenderer]  
#   def post( request, *args, **kwargs):
#     print("---------------------")
#     print(args)
#     print("....................")
#     user = Areas.objects.get(id=area_id)
#     serializer = AreaRegistrationSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
  



# class PermissionView(APIView):
#   permission_classes = (IsAuthenticated,)
#   def post(self, request, format=None):
#     print(f"Permission Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {request.data}")
#     serializer = PermissionSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     area = serializer.save()
#     return Response({'msg':'Permission Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class AreaRegistrationView(APIView):
#   permission_classes = (IsAuthenticated,)
#   renderer_classes = [AreaRenderer]

  def get(self, request):
    response = Areas.objects.all().values()

    return Response(response)

  def post(self, request, format=None):
    print("............................................")
    data = request.data.copy()

    # Validator
    if not stringValidator(data['area_name']):
      return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid area_name"})

    application_id = GetAppID()
    data['application'] = application_id
    serializer = AreaRegistrationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Areas Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)

class RolePermissionView(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self, request, format=None):
    print(f"Role Permission Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {request.data}")

    application_id = GetAppID()
    data = request.data.copy()
    data['application'] = application_id
    serializer = RolePermissionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Role Permission Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)


class RoleRegistrationView(APIView):

  def get(self, request):

    # Return all user roles
    response = UserRoles.objects.all().values()

    return Response(response)
  
  def post(self, request):

    # Get rolename from post request
    data = request.data.copy()

    print(data)
    # Validators
    if not stringValidator(data['rolename']):
      return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "rolename invalid"})
    # if not idValidator(data['role_category']):
    #   return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "role_category invalid"})
    if data['can_redistribute_power'].lower() not in ["yes", "no"]:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "can_redistribute_power invalid"})

    application_id = GetAppID()
    data['application'] = application_id

    serializer = UserRolesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Save rolename in the UserRoles table
    UserRoles(rolename=rolename).save()

    return Response(data={"result": "Role Added Succesfully"})

class AreaUpdateView(APIView):
#   permission_classes = (IsAuthenticated,)
  # renderer_classes = [AreaRenderer]
  def post(request, *args, **kwargs):
    print("---------------------")
    print(args)
    print("....................")
    user = Areas.objects.get(id=area_id)

    data = request.data.copy()
    application_id = GetAppID()
    data['application'] = application_id

    serializer = AreaRegistrationSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class PermissionView(APIView):
#   permission_classes = (IsAuthenticated,)

  def get(self, request):

    # Return all permissions in the permissions table
    response = Permissions.objects.all().values()
    return Response(response)

  def post(self, request, format=None):
    print(f"Permission Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {request.data}")

    data = request.data.copy()

    # Validators
    # Validation using idValidator for areas removed.
    
    if not stringValidator(request.data.get('permission_name')):
      return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid permission_name"})

    serializer = PermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Permission Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)


class RolePermissionView(APIView):
#   permission_classes = (IsAuthenticated,)
  def post(self, request, format=None):
    print(f"Role Permission Data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {request.data}")

    # Validators
    # if not idValidator(request.data.get('role')):
    #   return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid 'role'"})
    # if not idValidator(request.data.get('permission')):
    #   return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid 'permission'"})

    serializer = RolePermissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    area = serializer.save()
    return Response({'msg':'Role Permission Registration Successful','data':serializer.data}, status=status.HTTP_201_CREATED)

class PermissionsAreasView(APIView):

  def get(self, request):

    all_areas = Areas.objects.all().values()
    final_areas = []
    for i in all_areas:
      i['permissions'] = Permissions.objects.filter(areas_id=i['id']).values()
      final_areas.append(i)
    
    print(final_areas)

    return Response(final_areas)

class RolePermissions_Permissions_View(APIView):

  def post(self, request):

    # Get role_id from POST request
    role_id = request.data.get('role_id')

    # Validator
    # if not idValidator(role_id):
    #   return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid role_id"})

    # Get permissions_ids from RolePermissions for given role_id.
    response = RolePermissions.objects.filter(role_id = role_id).only("permission_id").values("permission_id")

    return Response(response)


class UpdatePermissions(APIView):

  def post(self, request, format=None):

    # Get permission_ids from POST request
    print(request.POST.get('permissions[0]'))
    role_id = request.data.get('role_id')
    print(role_id)
    # Validators
    # if not idValidator(role_id):
    #   return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid role_id"})
    # print(len(request.POST.getlist('permissions')))
    permission_ids = []
    for key, value in request.POST.items():
            if key.startswith('permissions[') and key.endswith(']'):
                permission_ids.append(int(value))

    # permission_ids = [int(request.POST.get(f'permissions[{i}]')) for i in range(len(request.POST.getlist('permissions')))]#request.POST.getlist('permissions')
    # permission_ids = request.data.get('permissions[0]')
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", permissions)
    # if type(permission_ids) is list:

    #   for permission_id in permission_ids:
    #     if not idValidator(permission_id):
    #       return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "invalid 'permission_ids'"})

    # Get permission_id from RolePermissions table for specified role_id
    permissions = RolePermissions.objects.filter(role_id = role_id)
    permission_values = [x[0] for x in permissions.values_list('permission_id')]

    # New permissions to be added
    add_permissions = set(permission_ids) - set(permission_values)

    # Permissions to be removed
    remove_permissions = set(permission_values) - set(permission_ids)

    # Add permissions - database
    # bulk saving possible? save operation for every row would be come at cost. maybe use raw sql. or manual commit after making all the queries.

    application_id = GetAppID()

    data = {"role": role_id, "application": application_id}
    for permission_id in add_permissions:

      data['permission'] = permission_id
      rolePermissionSerializer = RolePermissionSerializer(data=data)

      if rolePermissionSerializer.is_valid():
        rolePermissionSerializer.save()

      else:
        return Response(400)

    return Response(200)
      # RolePermissions(role_id = role_id, permission_id = permission_id, application=application_id).save()

    # Remove permissions - database
    # bulk deleting possible. maybe use raw sql. or manual commit after making all the delete queries.
    for permission_id in remove_permissions:
      rp = RolePermissions.objects.filter(role_id = role_id, permission_id = permission_id).delete()

    return Response(200)

