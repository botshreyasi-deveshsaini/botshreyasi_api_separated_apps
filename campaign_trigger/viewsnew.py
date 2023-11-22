from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from jobs.models import AddToJob, AddNewJob
from campaign.models import CampaignEvent, CampaignChannel
from .models import TriggerActionCampaign, ActionTrigger
from .serializers import TriggerActionCampaignSerializer, ActionTriggerSerializer
from .actions import *
from django.db.models import Q

class CampaignStart(APIView):
    def get(self, request):
        current_datetime = timezone.now()
        CandidatesInCampaign = AddToJob.objects.filter(
            Q(campaign_status=False) &
            (Q(campaign_run_time__lt=current_datetime) | Q(campaign_run_time__isnull=True)) &
            Q(is_deleted=False)
        )
        
        if CandidatesInCampaign.exists():
            for candidate in CandidatesInCampaign:
                self.process_event(candidate, 'startcampaign')
            return JsonResponse(f'All Event Done --> {current_datetime}', safe=False)
        else:
            return JsonResponse(f'Event not found --> {current_datetime}', safe=False)

    def process_event(self, candidate, campaignposition, parent_id=None):
        job = AddNewJob.objects.using('mysqlslave').get(id=candidate.job_id)
        candidate.client_department_id = job.department_id
        CampaignsData = CampaignEvent.objects.using('mysqlslave').filter(
            parent_id__isnull=True, campaign_id=candidate.campaign_id
        )
        
        for events in CampaignsData:
            print(events.event_name)
            atj_id = candidate.id
            candidate_status = self.check_action_condition(events, candidate, atj_id, campaignposition, parent_id)
            print(f"----------------> candidate data <------------------")
            self.log_candidate_status(candidate_status)

            add_to_job_data = {
                "id": candidate_status.id,
                "campaign_status": candidate_status.campaign_status
            }
            Addtojobserializer = AddToJobSerializer(candidate, data=add_to_job_data)
            if Addtojobserializer.is_valid():
                Addtojobserializer.save()
            else:
                print("Add To Serializer is not valid.")
                print(Addtojobserializer.errors)

    def check_action_condition(self, events, candidate, atj_id, campaignposition, parent_id=None):
        current_datetime = timezone.now()
        candidate_added_time = candidate.created_at
        print(events.event_type)
        if events.event_type == 'condition':
            if events.candidate_status_id == candidate.status_id:
                actionparam = [candidate.application_id, candidate.campaign_id, 0, events.id]
                NextCampaignAction = CampaignEvent.objects.using('mysqlslave').filter(
                    parent=events.id,
                    campaign=events.campaign_id,
                    application=events.application_id,
                    is_deleted=False
                )

                CreateActionDate = self.find_date(NextCampaignAction, candidate_added_time)
                for action in CreateActionDate:
                    next_action_time = action.action_time
                    if current_datetime > next_action_time:
                        move_to_trigger = self.move_to_campaign_trigger(action, candidate, atj_id, campaignposition, parent_id)
                        candidate.campaign_status = 1
                    else:
                        candidate.campaign_run_time = next_action_time
            else:
                print(f"Condition Not Matched: event status is {events.candidate_status_id} and candidate status is {candidate.status_id}")
        elif events.event_type == 'action':
            CreateActionDate = self.find_date([events], candidate_added_time)
            for action in CreateActionDate:
                next_action_time = action.action_time
                if current_datetime > next_action_time:
                    move_to_trigger = self.move_to_campaign_trigger(action, candidate, atj_id, campaignposition, parent_id)
                    candidate.campaign_status = 1
                    candidate.is_next_action = True
                else:
                    candidate.campaign_run_time = next_action_time
                    candidate.next_action_time = next_action_time
        else:
            print(f"Unsupported event type: {events.event_type}")

        return candidate

    def log_candidate_status(self, candidate_status):
        if candidate_status is not None:
            fields = candidate_status._meta.fields
            for field_name in fields:
                attr_value = getattr(candidate_status, field_name.name, None)
                print(f"{field_name.name}: {attr_value}")
        else:
            print("candidate status is None")

    def move_to_campaign_trigger(self, action, candidate, atj_id, campaignposition, parent_id=None):
        try:
            campaign_channel = CampaignChannel.objects.using('mysqlslave').get(id=action.channel_id)
        except CampaignChannel.DoesNotExist:
            print(f"error: Channel not found --> {action.channel_id}")

        trigger = {
            'action_name': campaign_channel.channel_name,
            'action_root_name': campaign_channel.channel_root_name,
            'action_temp_id': action.temp_id,
            'campaign': action.campaign_id,
            'candidate': candidate.candidate_id,
            'add_to_job': atj_id,
            'job': candidate.job_id,
            'client_department': candidate.client_department_id,
            'event': action.id,
            'user': candidate.user_id,
            'application': candidate.application_id,
            'parent': parent_id
        }

        action_trigger = TriggerActionCampaign.objects.filter(
            candidate_id=candidate.candidate_id,
            event=action.id,
            add_to_job=atj_id,
            campaign=action.campaign_id
        ).count()

        if action_trigger == 0:
            if campaignposition == 'startcampaign':
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
            if Triggerserializer.is_valid():
                Triggerserializer.save()
                print("Serializer is valid. Data saved.")
                return 'Data saved'
            else:
                print("Serializer is not valid.")
                print(Triggerserializer.errors)
                return "Serializer is not valid."
        else:
            print("candidate Already Trigger")
            return "candidate Already Trigger"

    def find_date(self, actions_Campaign, candidate_added_time):
        current_datetime = candidate_added_time
        action_time = None
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


class CreateNewAction(APIView):
    def get(self, request):
        current_datetime = timezone.now()
        actions = TriggerActionCampaign.objects.filter(
            Q(is_next_action=0) &
            (Q(next_action_time__lt=current_datetime) | Q(next_action_time__isnull=True)) &
            Q(is_action=1)
        )

        if actions.exists():
            for candidate in actions:
                print(f"action_id   ---> {candidate.id}")
                print(f"candidate.action_root_name ---> {candidate.action_root_name}")
                if candidate.action_root_name == "JumpToEvent":
                    CampaignsData = CampaignEvent.objects.using('mysqlslave').filter(id=candidate.action_temp_id)
                else:
                    CampaignsData = CampaignEvent.objects.using('mysqlslave').filter(parent_id=candidate.event_id)
                for events in CampaignsData:
                    atj_id = candidate.add_to_job_id
                    parent_id = candidate.id
                    campaignposition = 'nextevent'
                    candidate_status = self.check_action_condition(events, candidate, atj_id, campaignposition, parent_id)
                    print(candidate_status)
                    self.update_trigger_status(candidate, candidate_status)

            return JsonResponse(f'all Done at {current_datetime}', safe=False)
        else:
            print(f"error :--> Event not found ma --> {current_datetime}")
            return JsonResponse(f'Event not found man--> {current_datetime}', safe=False)

    def update_trigger_status(self, candidate, candidate_status):
        serializer = TriggerActionCampaignSerializer(candidate, data=candidate_status.__dict__)
        if serializer.is_valid():
            serializer.save()
        else:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(serializer.errors)

    def check_action_condition(self, events, candidate, atj_id, campaignposition, parent_id=None):
        current_datetime = timezone.now()
        candidate_added_time = candidate.created_at
        if events.event_type == 'condition':
            if events.candidate_status_id == candidate.status_id:
                actionparam = [candidate.application_id, candidate.campaign_id, 0, events.id]
                NextCampaignAction = CampaignEvent.objects.using('mysqlslave').filter(
                    parent=events.id,
                    campaign=events.campaign_id,
                    application=events.application_id,
                    is_deleted=False
                )

                CreateActionDate = self.find_date(NextCampaignAction, candidate_added_time)
                next_action_time = CreateActionDate[0].action_time if CreateActionDate else None

                if current_datetime > next_action_time:
                    self.move_to_trigger(candidate, CreateActionDate[0], atj_id, campaignposition, parent_id)
                    candidate.campaign_status = 1
            else:
                print(f"Condition Not Matched: event status is {events.candidate_status_id} and candidate status is {candidate.status_id}")
        elif events.event_type == 'action':
            CreateActionDate = self.find_date([events], candidate_added_time)
            next_action_time = CreateActionDate[0].action_time if CreateActionDate else None

            if current_datetime > next_action_time:
                self.move_to_trigger(candidate, CreateActionDate[0], atj_id, campaignposition, parent_id)
                candidate.campaign_status = 1
                candidate.is_next_action = True
            else:
                candidate.campaign_run_time = next_action_time
                candidate.next_action_time = next_action_time
        else:
            print(f"Unsupported event type: {events.event_type}")

        return candidate

    def move_to_trigger(self, candidate, action, atj_id, campaignposition, parent_id=None):
        try:
            campaign_channel = CampaignChannel.objects.using('mysqlslave').get(id=action.channel_id)
        except CampaignChannel.DoesNotExist:
            print(f"error :--> Channel  not found --> {action.channel_id}")

        trigger = {
            'action_name': campaign_channel.channel_name,
            'action_root_name': campaign_channel.channel_root_name,
            'action_temp_id': action.temp_id,
            'campaign': action.campaign_id,
            'candidate': candidate.candidate_id,
            'add_to_job': atj_id,
            'job': candidate.job_id,
            'client_department': candidate.client_department_id,
            'event': action.id,
            'user': candidate.user_id,
            'application': candidate.application_id,
            'parent': parent_id
        }

        action_trigger = TriggerActionCampaign.objects.filter(
            candidate_id=candidate.candidate_id,
            event=action.id,
            add_to_job=atj_id,
            campaign=action.campaign_id
        ).count()

        if action_trigger == 0:
            if campaignposition == 'startcampaign':
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
            if Triggerserializer.is_valid():
                Triggerserializer.save()
                print("Serializer is valid. Data saved.")
                return 'Data saved'
            else:
                print("Serializer is not valid.")
                print(Triggerserializer.errors)
                return "Serializer is not valid."
        else:
            print("candidate Already Trigger")
            return "candidate Already Trigger"

    def find_date(self, actions_Campaign, candidate_added_time):
        current_datetime = candidate_added_time
        action_time = None
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



class TriggerAction(APIView):
    def get(self, request):
        current_datetime = datetime.now()
        current_datetime_in_timezone = timezone.localtime(timezone.make_aware(current_datetime))
        actions = TriggerActionCampaign.objects.filter(Q(is_action=0) & Q(action_run_time__lt=current_datetime_in_timezone))
        if actions.exists():
            for action in actions:
                print(action.action_root_name)
                if action.action_root_name == 'JumpToEvent':
                    print(action.action_root_name)
                    event_status = TriggerAction.jump_to_event(action)  # Use TriggerAction class here
                elif action.action_root_name == 'call':
                    event_status = TriggerAction.call(action)  # Use TriggerAction class here
                elif action.action_root_name == 'email':
                    event_status = TriggerAction.mail(action)  # Use TriggerAction class here
                elif action.action_root_name == 'sms':
                    event_status = TriggerAction.sms(action)  # Use TriggerAction class here
                else:
                    # Handle other cases or provide a default action
                    event_status = {
                        "action_name": action.action_name,
                        "action_root_name": action.action_root_name,
                        "is_action": True,
                    }

                serializer = TriggerActionCampaignSerializer(action, data=event_status)
                if serializer.is_valid():
                    serializer.save()
                    print("Serializer is valid. Data saved.")
                else:
                    print("Serializer is not valid.")
                    print(serializer.errors)
        else:
            print('no data found')
        return Response('event done')
