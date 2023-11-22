from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView
from call.models import Calls
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import Chats
from datetime import datetime,timedelta
from .serializers import ChatSerializer
import uuid
# Create your views here.
class ChatBot(APIView):
    def get(self,request):
        call_id = request.GET.get('c')
        trigger_history_id = request.GET.get('cth')
        trigger_id = request.GET.get('ct')
        print(call_id)
        current_datetime = datetime.now()
        try:
            calldata = Calls.objects.using('mysqlslave').get(id=call_id)
            try:
                chat = Chats.objects.using('mysqlslave').get(call_id=call_id)
                print("manoj")
                return HttpResponseRedirect(f"http://127.0.0.1:8001/{chat.uid}/manoj")

            except Chats.DoesNotExist:
               print("Chat not Exist")
               chatdata = {
                  'app_id': calldata.application_id,
                  'job_id':calldata.job_id,
                #   'client_id':calldata.client_id
                  'recruiter_id':calldata.user_id,
                  'candidate_id':calldata.candidate_id,
                  'custom_data':str(calldata.custom_data),
                  'call_id':calldata.id,
                  'id':calldata.id,
                  'disposition':'tochat',
                  'link_open_count': 1,
                  'email_link_open_count':1,
                  'sms_link_open_count':1,
                  'chat_link_open_time':current_datetime,
                  'uid': str(uuid.uuid4()),
                  'campaign_trigger_history': trigger_history_id,
                  'campaign_trigger': trigger_id,
                  'call_history': calldata.call_history_id
               }
               chat_serializer = ChatSerializer(data=chatdata)
               if chat_serializer.is_valid():
                  chat_instanse = chat_serializer.save()
                  return HttpResponseRedirect(f"http://http:127.0.0.1:8001/{chat_instanse.uid}/")
                #   return JsonResponse(chat_instanse)
               else:
                  return JsonResponse(chat_serializer.errors)
                     
            # return JsonResponse(calldata, safe=False)
        except Calls.DoesNotExist:
         print("............")
        #  return JsonResponse({'error': 'Invalid Url'})
        return HttpResponseRedirect("https://botshreyasi.com/Invalid-Url")

        # print(calldata)
        # return Response(calldata)