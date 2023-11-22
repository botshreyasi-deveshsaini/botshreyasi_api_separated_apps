from django.shortcuts import render
from helper.views import GetStoreProcedureData,CalculateDatetimeInterval
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from jobs.serializer import AddToJobSerializer
from jobs.models import AddToJob
from campaign.models import CampaignChannel, CampaignEvent
from .serializers import TriggerActionCampaignSerializer
from .models import TriggerActionCampaign
# Create your views here.
def startcampaign(request):
    current_datetime = datetime.now()
    CandidatesInCampaign = GetStoreProcedureData('GetCandidateinCampaign', [])
    for candidate in CandidatesInCampaign:
        atj_id = candidate.get('id')
        user_id = candidate.get('user_id')
        application_id = candidate.get('application_id')
        campaign_id = candidate.get('campaign_id')
        event_id = candidate.get('campaign_event_id')
        campaign_status = candidate.get('campaign_status')
        candidate_added_time= candidate.get('created_at')
        campaign_run_time = candidate.get('campaign_run_time')
        candidate_status_id = candidate.get('status_id')
        candidate_id = candidate.get('candidate_id')
        params = [application_id, campaign_id, event_id, 0]
        CampaignsData = GetStoreProcedureData('GetCampaignEventsToRunCampaign', params)
        for events in CampaignsData:
            if events.get('event_type') == 'condition':
                if events.get('candidate_status_id') == candidate_status_id:
                    actionparam = [application_id, campaign_id, 0, events.get('id')]
                    NextCampaignAction = GetStoreProcedureData('GetCampaignEventsToRunCampaign', actionparam)
                    CreateActionDate = find_date(NextCampaignAction)
                    for action in CreateActionDate:
                        next_action_time= candidate_added_time  + action['action_time']
                        print(f"next_action_time --> {next_action_time}")
                        try:
                            addtojob = AddToJob.objects.using('mysqlslave').get(id=atj_id)
                        except AddToJob.DoesNotExist:
                            print(f"error :--> Event not found --> {atj_id}")
                        if current_datetime > next_action_time:
                            try:
                                campaign_channel = CampaignChannel.objects.using('mysqlslave').get(id=action['temp_id'])
                            except CampaignChannel.DoesNotExist:
                                print(f"error :--> Channel  not found --> {action['channel_id']}")
                            print(f"campaign_channel name ---> {campaign_channel.id}")
                            trigger = {'action_name': campaign_channel.channel_name,
                                       'action_root_name':campaign_channel.channel_root_name,
                                       'action_temp_id':action['temp_id'],
                                       'next_action_time': datetime(2023, 12, 31, 12, 0, 0),
                                       'campaign':action['campaign_id'],
                                       'candidate':candidate_id,
                                       'add_to_job':atj_id,
                                       'event':action['id'],
                                       'user':user_id,
                                       'application':application_id
                                       }
                            action_trigger = TriggerActionCampaign.objects.filter(candidate_id=candidate_id, event=action['id'],add_to_job=atj_id).count()
                            if action_trigger == 0:
                                Triggerserializer = TriggerActionCampaignSerializer(data=trigger)
                                print(Triggerserializer)
                                if Triggerserializer.is_valid():
                                    Triggerserializer.save()
                                    print("Serializer is valid. Data saved.")
                                else:
                                    # If the serializer is not valid, you can print error messages or take appropriate action
                                    print("Serializer is not valid.")
                                    print(Triggerserializer.errors)
                            candidate['campaign_status'] = 1
                            serializer = AddToJobSerializer(addtojob, data=candidate)
                            if serializer.is_valid():
                                serializer.save()
                            print(trigger)
                        else:
                            candidate['campaign_run_time'] = next_action_time
                            serializer = AddToJobSerializer(addtojob, data=candidate)
                            if serializer.is_valid():
                                serializer.save()
                else:
                    print("Condition Not Match")
            elif events.get('event_type') == 'action':
                CreateActionDate = find_date(NextCampaignAction)

            else:
                print("somthing went wrong")
    return JsonResponse(f'all Done at {current_datetime}', safe=False)

def find_date(actions_Campaign):
    current_datetime = datetime.now()
    for nextaction in actions_Campaign:
        if nextaction.get('trigger_mode') == 'immediate':
            action_time = current_datetime
        elif nextaction.get('trigger_mode') == 'interval':
            action_time = CalculateDatetimeInterval(
                nextaction.get('trigger_interval'),
                nextaction.get('trigger_interval_unit')
            )
        elif nextaction.get('trigger_mode') == 'date':
            action_time = nextaction.get('trigger_date')
        nextaction['action_time'] = action_time
    actions_Campaign.sort(key=lambda x: x['action_time'])
    return actions_Campaign




class TriggerAction(APIView):
    def get(self,request):
        current_datetime = datetime.now()
        actions = TriggerActionCampaign.objects.using('mysqlslave').filter(is_action=0)
        if actions.exists():
            print(actions[0].id)
            for action in actions:
                # print(action.id)
                if action.action_root_name == 'JumpToEvent':
                   print(action.action_root_name)
                   self.jump_to_event(action)

        else:
            print('no data found')

    def jump_to_event(self,action):
        try:
            event = CampaignEvent.objects.using('mysqlslave').get(id=action.action_temp_id)
            print(event.id)
            CreateActionDate = find_date(event)
            print(CreateActionDate)

        except CampaignEvent.DoesNotExist:
            print("event not found") 
        

        


