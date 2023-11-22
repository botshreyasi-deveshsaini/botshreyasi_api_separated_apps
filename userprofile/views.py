from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from helper.views import *
from django.core.exceptions import ValidationError


@method_decorator(csrf_exempt,name='dispatch')
class getProfile(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        print("manoj")
        User = getUser()
        application = GetApplication()
        User['application'] = application['application_name']
        return Response(User)

class getTeam(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        application_id = GetAppID()
        print("<============================================>")
        print(f"application_id:--------------------------------------> {application_id}")
        user_id = GetUserID()
        print(f"user_id:--------------------------------------> {user_id}")
        child_roles = GetChild(application_id, user_id)
        print(f"child_roles:-----------------------> {child_roles}")
        if not child_roles:
            child_roles = [user_id]
        else:
            child_roles = [int(role_id) for role_id in child_roles]

        print(f"child_roles:-----------------------> {child_roles}")
        print("<============================================>")
        try:
            users = User.objects.filter(application=application_id, id__in=child_roles)
        except ValidationError as e:
            response_data = {'error': str(e)}
            return Response(response_data, status=400)
        print(f"users:--------------------------------------> {users}")

        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'name': user.name,
                # Include other user fields as needed
            })
    
        return JsonResponse(user_data, safe=False)