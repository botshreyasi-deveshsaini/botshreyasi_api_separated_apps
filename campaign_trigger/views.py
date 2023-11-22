from django.shortcuts import render
from helper.views import GetStoreProcedureData,CalculateDatetimeInterval,prepare_message, generate_key
from datetime import datetime,timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from jobs.serializer import AddToJobSerializer
from jobs.models import AddToJob, AddNewJob
from campaign.models import CampaignChannel, CampaignEvent
from .serializers import TriggerActionCampaignSerializer, ActionTriggerSerializer
from .models import TriggerActionCampaign,ActionTrigger
from django.core import serializers
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from .actions import *


class CampaignStart(APIView):
    def get(self,request):
        current_datetime = datetime.now()
        current_datetime_in_timezone = timezone.localtime(timezone.make_aware(current_datetime))
        CandidatesInCampaign = AddToJob.objects.filter(Q(campaign_status=False) & (Q(campaign_run_time__lt=current_datetime_in_timezone) | Q(campaign_run_time__isnull=True)) & Q(is_deleted = False))
        if CandidatesInCampaign.exists():
            for candidate in CandidatesInCampaign:
                job = AddNewJob.objects.using('mysqlslave').get(id=candidate.job_id)
                candidate.client_department_id = job.department_id
                CampaignsData = CampaignEvent.objects.using('mysqlslave').filter(parent_id__isnull=True, campaign_id =candidate.campaign_id)
                for events in CampaignsData:
                    print(events.event_name)
                    atj_id = candidate.id
                    campaignposition = 'startcampaign'
                    candidate_status =check_action_condition(events, candidate,CandidatesInCampaign,atj_id,campaignposition)
                    print(f"----------------> candidate data <------------------")
                    if candidate_status is not None:
                        fields = candidate_status._meta.fields
                        for field_name in fields:
                            attr_value = getattr(candidate_status, field_name.name, None)
                            print(f"{field_name.name}: {attr_value}")
                    else:
                        print("cadidate status is none")
                    add_to_job_data = {
                        "id" : candidate_status.id,
                        "campaign_status" : candidate_status.campaign_status
                    }
                    Addtojobserializer = AddToJobSerializer(candidate, data=add_to_job_data)
                    if Addtojobserializer.is_valid():
                        Addtojobserializer.save()
                    else:
                        print("Add To Serializer is not valid.")
                        print(Addtojobserializer.errors)
            return JsonResponse(f'All Event Done --> {current_datetime}', safe=False)

        else:
            return JsonResponse(f'Event not found --> {current_datetime}', safe=False)


class CreateNewAction(APIView):
    def get(self,request):
        current_datetime = datetime.now()
        current_datetime_in_timezone = timezone.localtime(timezone.make_aware(current_datetime))
        actions = TriggerActionCampaign.objects.filter(Q(is_next_action=0) & Q(is_ready_to_next_event=1) & (Q(next_action_time__lt=current_datetime_in_timezone) | Q(next_action_time__isnull=True)) & Q(is_action=1))
        if actions.exists():
            for candidate in actions:
                print(f"action_id   ---> {candidate.id}")
                print(f"candidate.action_root_name ---> {candidate.action_root_name}")
                if candidate.action_root_name == "JumpToEvent":
                    CampaignsData = CampaignEvent.objects.using('mysqlslave').filter(id=candidate.action_temp_id)
                else:
                    CampaignsData = CampaignEvent.objects.using('mysqlslave').filter(parent_id=candidate.event_id)
                print(CampaignsData)
                for events in CampaignsData:
                    atj_id = candidate.add_to_job_id
                    parent_id = candidate.id
                    campaignposition = 'nextevent'
                    candidate_status = check_action_condition(events, candidate,actions,atj_id,campaignposition,parent_id)
                    print(candidate_status)
                    serializer = TriggerActionCampaignSerializer(candidate, data=candidate_status.__dict__)
                    if serializer.is_valid():
                        serializer.save()
                        print("data update")
                    else:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        print(serializer.errors)
            return JsonResponse(f'all Done at {current_datetime}', safe=False)
        else:
            print(f"error :--> Event not found ma --> {current_datetime_in_timezone}")
            return JsonResponse(f'Event not found man--> {current_datetime}', safe=False)

class TriggerAction(APIView):
    def get(self,request):
        current_datetime = datetime.now()
        current_datetime_in_timezone = timezone.localtime(timezone.make_aware(current_datetime))
        actions = TriggerActionCampaign.objects.filter(Q(is_action=0) & Q(action_run_time__lt = current_datetime_in_timezone))
        if actions.exists():
            for action in actions:
                print(action.action_root_name)
                if action.action_root_name == 'JumpToEvent':
                    print(action.action_root_name)
                    event_status = CampaignActions.jump_to_event(self,action)
                elif action.action_root_name == 'call':
                    event_status = CampaignActions.call(self,action)
                elif action.action_root_name == 'email':
                    event_status = CampaignActions.mail(self,action)
                elif action.action_root_name == 'sms':
                    event_status = CampaignActions.sms(self,action)
                elif action.action_root_name == 'emailsms':
                    event_status = CampaignActions.sms(self,action)
                    event_status = CampaignActions.mail(self,action)
                elif action.action_root_name =='latercall':
                    event_status =CampaignActions.later_call(self,action)
            
                
                # else:
                #     event_status = {
                #         "action_name": action.action_name,
                #         "action_root_name": action.action_root_name,
                #         "is_action": True,
                #     }
            
            serializer = TriggerActionCampaignSerializer(action, data=event_status)
            if serializer.is_valid():
                trigger_insc = serializer.save()
                print(trigger_insc.action_run_time)
                print("Serializer is valid. Data saved.")
            else:
                print("Serializer is not valid.")
                print(serializer.errors)
        else:
            print('no data found')
        return Response('event done')



def check_action_condition(events, candidate, CandidatesInCampaign, atj_id, campaignposition, parent_id=None):
    current_datetime = datetime.now()
    current_datetime_in_timezone = timezone.localtime(timezone.make_aware(current_datetime))
    candidate_added_time = candidate.created_at
    print(events.event_type)
    if events.event_type == 'condition':
        if events.candidate_status_id == candidate.status_id:
            print(f"Condition Matched: event status is {events.candidate_status_id} and candidate status is {candidate.status_id}  --> trigger_id {candidate.id}")
            actionparam = [candidate.application_id, candidate.campaign_id, 0, events.id]
            print(f"(parent={events.id}, campaign={events.campaign_id}, application={events.application_id}, is_deleted=False)")
            NextCampaignAction = CampaignEvent.objects.using('mysqlslave').filter(parent=events.id, campaign=events.campaign_id, application=events.application_id, is_deleted=False)
            print("1111111111111111111111111111111111111")
            CreateActionDate = find_date(NextCampaignAction,candidate_added_time)
            for action in CreateActionDate:
                print("******************************")
                print(f"{action.action_time}")
                print("******************************")
                next_action_time =  action.action_time
                print(f"{current_datetime_in_timezone} > {next_action_time}")
                if current_datetime_in_timezone > next_action_time:
                    move_to_trigger = move_to_campaign_trigger(action, candidate, atj_id,campaignposition, parent_id)
                    candidate.campaign_status = 1
                    candidate.is_next_action = True
                    print(f"manoj --------> candidate.campaign_status ------->  {candidate.campaign_status}")
                else:
                    candidate.campaign_run_time = next_action_time
        else:
            print(f"Condition Not Match: event status is {events.candidate_status_id} and candidate status is {candidate.status_id}")
    elif events.event_type == 'action':
        CreateActionDate = find_date([events], candidate_added_time)
        print("date Done")
        for action in CreateActionDate:
            print(f"{candidate_added_time} + {action.action_time}")
            next_action_time = action.action_time
            if current_datetime_in_timezone > next_action_time:
                move_to_trigger = move_to_campaign_trigger(action, candidate, atj_id,campaignposition, parent_id)
                candidate.campaign_status = 1
                candidate.is_next_action = True
            else:
                candidate.campaign_run_time = next_action_time
                candidate.next_action_time = next_action_time
    else:
        print(f"{events.event_type} is not defined in our database")

    return candidate  # This is not necessary if you are modifying the 'candidate' object directly

def move_to_campaign_trigger(action,candidate,atj_id,campaignposition,parent_id=None):
    print("----------->move_to_campaign_trigger<-------------")
    try:
        print("manoj")
        campaign_channel = CampaignChannel.objects.using('mysqlslave').get(id=action.channel_id)
    except CampaignChannel.DoesNotExist:
        print(f"error :--> Channel  not found --> {action.channel_id}")
    print(f"campaign_channel name ---> {campaign_channel.id}")
    trigger = {'action_name': campaign_channel.channel_name,
               'action_root_name':campaign_channel.channel_root_name,
               'action_temp_id':action.temp_id,
               'campaign':action.campaign_id,
               'candidate':candidate.candidate_id,
               'add_to_job':atj_id,
               'job': candidate.job_id,
               'client_department':candidate.client_department_id, 
               'event':action.id,
               'user':candidate.user_id,
               'application':candidate.application_id,
               'parent': parent_id
               }

    action_trigger = TriggerActionCampaign.objects.filter(candidate_id=candidate.candidate_id, event=action.id,add_to_job=atj_id,campaign=action.campaign_id).count()
    if action_trigger == 0:
        if(campaignposition == 'startcampaign'):
            Triggerserializer = ActionTriggerSerializer(data=trigger)
            if Triggerserializer.is_valid():
                trigger_instance = Triggerserializer.save()
                trigger['trigger'] = trigger_instance.id
                print("Serializer is valid. Data saved.")
            else:
                print("Serializer is not valid.")
                print(Triggerserializer.errors)
        else:
            Campaign_trigger = TriggerActionCampaign.objects.get(id=parent_id)
            trigger['trigger'] = Campaign_trigger.trigger_id
        Triggerserializer = TriggerActionCampaignSerializer(data=trigger)
        # print(Triggerserializer)
        if Triggerserializer.is_valid():
            Triggerserializer.save()
            print("Serializer is valid. Data saved.")
            return f'Data saved'
        else:
            print("Serializer is not valid.")
            print(Triggerserializer.errors)
            return "Serializer is not valid."
    else: 
        print("candidate Already Trigger")
        return "candidate Already Trigger"
    


def find_date(actions_Campaign, candidate_added_time):
    current_datetime = candidate_added_time
    print(current_datetime)
    print("----------->")
    action_time =None
    print(actions_Campaign)
    for nextaction in actions_Campaign:
        print(nextaction.event_name)
        print(nextaction.trigger_mode)
        if nextaction.trigger_mode == 'immediate':
            action_time = current_datetime
        elif nextaction.trigger_mode == 'interval':
            action_time = CalculateDatetimeInterval(
                nextaction.trigger_interval,
                nextaction.trigger_interval_unit
            )
        elif nextaction.trigger_mode == 'date':
            action_time = nextaction.trigger_date
        nextaction.action_time = action_time
        print(action_time)
    
    sorted_actions_Campaign = sorted(actions_Campaign, key=lambda x: x.action_time if hasattr(x, 'action_time') else datetime.max)
        
    return sorted_actions_Campaign
