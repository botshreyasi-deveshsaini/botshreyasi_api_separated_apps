from call.models import Calls
from chat.models import Chats
from rest_framework.views import APIView
from django.db.models import Q
from datetime import datetime,timedelta
from rest_framework.response import Response
from .models import TriggerActionCampaign,ActionTrigger
from .serializers import TriggerActionCampaignSerializer, ActionTriggerSerializer
from candidate_status.models import CandidateStatus
from call.serializers import CallSerializer
from chat.serializers import ChatSerializer
from email_log.models import EmailsLogs
from message_log.models import SMSLogs
from django.http import JsonResponse

import sys
class UpdateData(APIView):
    def get(self,request):
       call_status = update_call_status()
       chat_status = update_chat_status()
       mail_status = update_mail_status()
       return Response("all Done")
    
def update_call_status():
    current_datetime = datetime.now()
    Calls_data = Calls.objects.filter(Q(is_update=10) & Q(campaign_trigger_id__isnull=False))
    if Calls_data.exists():
        try:
            for call_data in Calls_data:
                if((call_data.call_status=='Failed' or call_data.call_status == 'Busy' or call_data.call_status == 'Ring Timeout') and call_data.disposition=='No Status'):
                    print("-----------> 1")
                    trigger = getstatus("CallNotConnect",call_data)
                    trigger['later_time'] = call_data.latter
                elif(call_data.call_status=='connected' and call_data.disposition=='Profile interested' and call_data.is_completed==True):
                    print("-----------> 2")
                    trigger = getstatus("ProfileIntersted",call_data)
                    trigger['later_time'] = call_data.latter
                elif(call_data.call_status=='connected' and (call_data.disposition=='Profile interested' or call_data.disposition=='job change intersted' or call_data.disposition=='Job Change interested') and call_data.is_completed==False):
                    print("-----------> 3")
                    trigger = getstatus("CallNotComplete",call_data)
                    trigger['later_time'] = call_data.latter
                elif(call_data.call_status=='connected' and call_data.disposition=='No Status'):
                    print("-----------> 4")
                    trigger = getstatus("NoStatus",call_data)
                    trigger['later_time'] = call_data.latter
                elif(call_data.call_status=='connected' and call_data.disposition=='Not interested'):
                    print("-----------> 5")
                    trigger = getstatus("NotInterested",call_data)
                    trigger['later_time'] = call_data.latter
                elif(call_data.call_status=='connected' and call_data.disposition=='Call Later'):
                    print("-----------> 6")
                    trigger = getstatus("CallLater",call_data)
                    trigger['later_time'] = call_data.latter
                else:
                    print("-----------> 7")
                    print(f"call_status ---> {call_data.call_status} , disposition --> {call_data.disposition} , is_completed ---> {call_data.is_completed} ")
                print(call_data.campaign_trigger_id)
                print()
                campaign_trigger_data = TriggerActionCampaign.objects.get(id=call_data.campaign_trigger_history_id)
                try:
                    trigger['action_name']=campaign_trigger_data.action_name
                    trigger['action_root_name']=campaign_trigger_data.action_root_name
                    action_trigger_update_history = TriggerActionCampaignSerializer(campaign_trigger_data, data=trigger)
                    if action_trigger_update_history.is_valid():
                        action_trigger_update_history.save()
                    else:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        print(action_trigger_update_history.errors)
                    # campaign_trigger  = ActionTrigger.objects.get(cam)
                    action_trigger_update = ActionTriggerSerializer(campaign_trigger_data.trigger,data=trigger)
                    if action_trigger_update.is_valid():
                        action_trigger_update.save()
                    else:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> action_trigger_update")
                        print(action_trigger_update.errors)
                    call={'is_update':1}
                    call_update = CallSerializer(call_data,data=call,partial=True)
                    if call_update.is_valid():
                        callupdate = call_update.save()
                        print("Call Update")
                except campaign_trigger_data.DoesNotExist:
                    print("campaign_trigger Not Found")
            return Response("all Done")
        except Exception as e:
            etype, evalue, tb = sys.exc_info()
            print("An error occurred:", e)
            print('Exception=>',e,f'  Line:{tb.tb_lineno}')
    else:
        # return Response(f'Event not found --> {current_datetime}', safe=False)
        return JsonResponse({'message': f'Event not found --> {current_datetime}'}, safe=False)

        
def update_chat_status():
    current_datetime = datetime.now()
    Chats_data = Chats.objects.using('mysqlslave').filter(Q(is_update=10) | Q(campaign_trigger_id__isnull=False))
    if Chats_data.exists():
        try:
            for chat_data in Chats_data:
                chat_data.application = chat_data.app_id
                print(chat_data.application)
                if( chat_data.disposition=='Profile interested' and chat_data.is_completed==True):
                    print("-----------> 2")
                    trigger = getstatus("ProfileIntersted",chat_data)
                elif(chat_data.disposition=='Not interested' and chat_data.is_completed==True):
                    print("-----------> 5")
                    trigger = getstatus("NotInterested",chat_data)
                else:
                    print("-----------> 7")
                    # print(f"disposition --> {chat_data.disposition} , is_completed ---> {call_data.is_completed} ")
                # print(chat_data.campaign_trigger_id)
                campaign_trigger_data = TriggerActionCampaign.objects.get(id=chat_data.campaign_trigger_history_id)
                try:
                    trigger['action_name']=campaign_trigger_data.action_name
                    trigger['action_root_name']=campaign_trigger_data.action_root_name
                    action_trigger_update_history = TriggerActionCampaignSerializer(campaign_trigger_data, data=trigger)
                    if action_trigger_update_history.is_valid():
                        action_trigger_update_history.save()
                        print("save")
                    else:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        print(action_trigger_update_history.errors)
                    action_trigger_update = ActionTriggerSerializer(campaign_trigger_data.trigger,data=trigger)
                    if action_trigger_update.is_valid():
                        action_trigger_update.save()
                    else:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> action_trigger_update")
                        print(action_trigger_update.errors)
                except campaign_trigger_data.DoesNotExist:
                    print("campaign_trigger Not Found")
                Chats.objects.filter(id=chat_data.id).update(is_update=1)
            return Response("all Done")
        except Exception as e:
            etype, evalue, tb = sys.exc_info()
            print("An error occurred:", e)
            print('Exception=>',e,f'  Line:{tb.tb_lineno}')
    else:
        # return Response(f'Event not found --> {current_datetime}', safe=False)
        return JsonResponse({'message': f'Chat Event not found --> {current_datetime}'}, safe=False)



def update_mail_status():
    current_datetime = datetime.now()
    Emails_data = EmailsLogs.objects.using('mysqlslave').filter(Q(is_update=10) & Q(campaign_trigger_history_id__isnull=False))
    if Emails_data.exists():
        try:
            for email_data in Emails_data:
                if(email_data.is_send==1 and email_data.is_read==False):
                    trigger = getstatus("EmailNotOpen",email_data)
                elif(email_data.is_send==1 and email_data.is_read==True):
                    trigger = getstatus("EmailOpen",email_data)
                try:
                     campaign_trigger_data = TriggerActionCampaign.objects.get(id=email_data.campaign_trigger_history_id)
                     findstatus = CandidateStatus.objects.using('mysqlslave').get(id=campaign_trigger_data.status_id)
                     if(findstatus.root_name != 'LinkClick' or findstatus.root_name != 'ProfileIntersted' or findstatus.root_name !='NotInterested'):
                         trigger['action_name']=campaign_trigger_data.action_name
                         trigger['action_root_name']=campaign_trigger_data.action_root_name
                         action_trigger_update_history = TriggerActionCampaignSerializer(campaign_trigger_data, data=trigger)
                         if action_trigger_update_history.is_valid():
                             action_trigger_update_history.save()
                         else:
                             print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                             print(action_trigger_update_history.errors)
                except campaign_trigger_data.DoesNotExist:
                    print("campaign_trigger Not Found")
                EmailsLogs.objects.filter(id=email_data.id).update(is_update=1)
        except Exception as e:
            etype, evalue, tb = sys.exc_info()
            print("An error occurred:", e)
            print('Exception=>',e,f'  Line:{tb.tb_lineno}')
    else:
        # return Response(f'Event not found --> {current_datetime}', safe=False)
        return JsonResponse({'message': f'Mail Event not found --> {current_datetime}'}, safe=False)

    
class UpdateSMSStatus(APIView):
    def get(self,request):
        current_datetime = datetime.now()
        messages_data = SMSLogs.objects.using('mysqlslave').filter(Q(is_update=10) | Q(campaign_trigger_id__isnull=False))
        if messages_data.exists():
            try:
                for mesage_data in messages_data:
                    if(mesage_data.is_send==1 and mesage_data.is_read==False):
                        trigger = getstatus("EmailNotOpen",mesage_data)
                    elif(mesage_data.is_send==1 and mesage_data.is_read==True):
                        trigger = getstatus("EmailOpen",mesage_data)
                    try:
                         campaign_trigger_data = TriggerActionCampaign.objects.get(id=mesage_data.campaign_trigger_history_id)
                         findstatus = CandidateStatus.objects.using('mysqlslave').get(id=campaign_trigger_data.status)
                         if(findstatus.root_name != 'LinkClick' or findstatus.root_name != 'ProfileIntersted' or findstatus.root_name !='NotInterested'):
                             trigger['action_name']=campaign_trigger_data.action_name
                             trigger['action_root_name']=campaign_trigger_data.action_root_name
                             action_trigger_update_history = TriggerActionCampaignSerializer(campaign_trigger_data, data=trigger)
                             if action_trigger_update_history.is_valid():
                                 action_trigger_update_history.save()
                             else:
                                 print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                 print(action_trigger_update_history.errors)
                    except campaign_trigger_data.DoesNotExist:
                        print("campaign_trigger Not Found")
                    SMSLogs.objects.filter(id=mesage_data.id).update(is_update=1)
            except Exception as e:
                etype, evalue, tb = sys.exc_info()
                print("An error occurred:", e)
                print('Exception=>',e,f'  Line:{tb.tb_lineno}')

        
        else:
            return Response(f'Event not found --> {current_datetime}', safe=False)

def getstatus(rootname, call_data):
    trigger = {}
    status = CandidateStatus.objects.using('mysqlslave').filter(root_name=rootname,application=call_data.application).first()
    if status:
        trigger['status'] = status.id
        trigger['status_name'] = status.root_name
        trigger['is_ready_to_next_event'] = 1
        print(status.root_name)
        print(status.id)  
        return trigger
    else:
        return trigger
