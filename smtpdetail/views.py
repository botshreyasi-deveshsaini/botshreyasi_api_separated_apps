from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from helper.views import *
from smtpdetail.models import SMTPDetails
from smtpdetail.serializers import SMTPSerializer

@method_decorator(csrf_exempt,name='dispatch')
class SMTPdetails(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request):
        print(f"SMTP Details:-->>>>>>>>>>>>>>>>>>>>>>>>{request.data}")
        mutable_data = request.data.copy()
        mutable_data['application'] = GetAppID()
        mutable_data['creater'] = GetUserID()
        serializer = SMTPDetails(data=mutable_data)
        if serializer.is_valid():
          Job = serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

    def get(self,request,*args,**kwargs):
        app_id = GetAppID()
        try:
            smtpdetails = SMTPSerializer(SMTPDetails.objects.get(application=app_id)).data
        except:
            smtpdetails =[]
        return Response(smtpdetails)
