from django.shortcuts import render

# Create your views here.
from functools import partial
from rest_framework import generics, status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from .serializers import *
from .models import *
from django.http import JsonResponse,HttpResponse
from helper.views import *
# Create your views here.

@method_decorator(csrf_exempt,name='dispatch')
class MESSAGE_TEMPLATE(APIView):
    def post(self,request):
        # try:
                data=request.data
                print("manoj:::::::::::::::::::::::::::::::::::::::::::")
                mutable_data = request.data.copy()
                mutable_data['application'] = GetAppID()
                mutable_data['added_by'] = GetUserID()
                Messagetempelate_email = Messagetemplate_email_serializer(data=mutable_data)
                if Messagetempelate_email.is_valid(raise_exception=True):
                   Job = Messagetempelate_email.save()
                   return HttpResponse(Messagetempelate_email.data, status=status.HTTP_201_CREATED)
                return HttpResponse(Messagetempelate_email.errors, status=status.HTTP_400_BAD_REQUEST)

        # except as e:
            # return Response("THIS IS NOT CORRECT WAY TO REQUEST")

@method_decorator(csrf_exempt,name='dispatch')
class GET_MESSAGE_TEMPLATE(APIView):
    def get(self,request):
        try:
            data=request.data
            appid=data["app_id"]
            addedby=data["addedby"]
            message=MessageTemplates.objects.filter(app_id = appid, addedby=addedby)
            return Response(message.values())
        except:
            return Response("THIS IS NOT CORRECT WAY TO REQUEST")

@method_decorator(csrf_exempt,name='dispatch')
class DELETE_MESSAGE_TEMPLATE(APIView):
    def delete(self,request):
        data=request.data
        appid=data["app_id"]
        id=data["id"]
        addedby=data["addedby"]
        message=MessageTemplates.objects.filter(id=id, app_id = appid, addedby=addedby)
        message.delete()
        return Response("DATA DELETED SUCCESFULLY")

@method_decorator(csrf_exempt,name='dispatch')
class UPDATE_MESSAGE_TEMPLATE(APIView):
    def patch(self,request):
        data=request.data
        obj=MessageTemplates.objects.get(id=data["id"])
        update_data={"id":"","title":"","message":"","templatename":"","dlt_te_id":""}
        update_data["id"]=data["id"]
        update_data["title"]=data["title"]
        update_data["message"]=data["message"]
        update_data["templatename"]=data["templatename"]
        update_data["dlt_te_id"]=data["dlt_te_id"]
        Messagetempelate_sms = Messagetemplate_sms_serializer(obj,data=update_data, partial= True)
        if Messagetempelate_sms.is_valid(raise_exception=True):
                Messagetempelate_sms.save()
                return Response("UPDATE DATA SUCCESSFULLY")

