from bot.models import BotDetails
from campaign.models import CampaignEvent
from helper.views import GetStoreProcedureData,prepare_message,generate_key,CalculateDatetimeInterval
from rest_framework.views import APIView
import json
from email_log.models import EmailTemplates,EmailsLogs
from email_log.serializers import EmailTemplates_serializer, EmailLogs_serializer
from message_log.models import SMSLogs,SmsTemplates
from message_log.serializers import SmsLogs_serializer
from call.views import CreateCustomData
from call.serializers import CallSerializer, CallsHistoriesSerializer
from datetime import datetime,timedelta
from django.utils import timezone

from call.models import Calls,CallsHistories
from url_shortner.models import UrlShortners

class CampaignActions(APIView):
    def __init__(self) -> None:
        self.datas = "manoj"

    def jump_to_event(self,action):
        print("Jump To Event --------------------------------------->")
        print(action.action_temp_id)
        try:
            event = CampaignEvent.objects.filter(id=action.action_temp_id)
            event = find_date(event,action.created_at)
            print(f"{action.created_at} + {event[0].action_time}")
            data_to_update = {
                "action_name": action.action_name,
                "action_root_name": action.action_root_name,
                "next_action_time": event[0].action_time,
                "is_ready_to_next_event": True,
                "is_action": True,
                }
            return data_to_update
        except CampaignEvent.DoesNotExist:
            print("event not found")

    def call(self,action):
        print("Call --------------------------------------->")
        try:
            # Botdetail = BotDetails.objects.using('mysqlslave').filter(id=action.action_temp_id, is_deleted=False).first()
            event = CampaignEvent.objects.get(id=action.event_id)
            Botdetail = BotDetails.objects.using('mysqlslave').filter(id=event.bot_id, is_deleted=False).first()
            if Botdetail:
                print(f"id -----------> {Botdetail.id}")
                params = [action.application_id, action.add_to_job_id]
                JobAndApplicationDetails = GetStoreProcedureData('GetCandidatesDetails', params)
                candidate_details = JobAndApplicationDetails[0]
                custom_data = CreateCustomData(Botdetail.custom_data, candidate_details)
                data = {}
                data['candidate'] = action.candidate_id
                data['custom_data'] = json.loads(custom_data)
                data['mobile_no'] = candidate_details['mobile_no']
                data['country_code'] = candidate_details['country_code']
                data['bot_status'] = 11
                data['user'] = candidate_details['user_id']
                data['application'] = candidate_details['application_id']
                data['call_to'] = Botdetail.file_name
                data['job'] = candidate_details['job_id']
                data['campaign_trigger'] = action.trigger_id
                data['campaign_trigger_history'] = action.id
                data['campaign'] = action.campaign_id
                data['campaign_event'] = action.event_id
                try:
                    findcallhistory = CallsHistories.objects.using('mysqlslave').get(campaign_trigger_id = action.trigger_id)
                    data['call_history_id'] = findcallhistory.id
                except CallsHistories.DoesNotExist:
                    call_history_serializer = CallsHistoriesSerializer(data=data)
                    if call_history_serializer.is_valid():
                        call_history_instance = call_history_serializer.save()
                        data['call_history_id'] = call_history_instance.id
                    else:
                        print(call_history_serializer.errors)

                serializer = CallSerializer(data=data)
                if serializer.is_valid():
                    print("call call")
                    call_instance = serializer.save()
                else:
                    print(serializer.errors)
            print("SEND Call")
            data_to_update = {
                "action_name": action.action_name,
                "action_root_name": action.action_root_name,
                "is_action": True,
                }
            return data_to_update
        except CampaignEvent.DoesNotExist:
            print("event not found")

    def later_call(self,action):
        print("-----------------------> Latercall <--------------------------------")
        print(action.action_temp_id)
        try:
            print("...,,,")
            call = Calls.objects.using('mysqlslave').filter(campaign_event_id=action.action_temp_id , candidate_id= action.candidate_id).first()
            print(call.id)
            current_datetime = datetime.now()
            # current_datetime = timezone.make_naive(current_datetime, timezone.utc)
            # current_datetime = timezone.make_naive(current_datetime, timezone.utc)
            current_datetime = current_datetime.replace(tzinfo=timezone.utc)

            print(current_datetime)
            print(f"latter Time : {call.latter}")
            if current_datetime < call.latter:
                print("manoj")
                data_to_update = {
                    "action_name": action.action_name,
                    "action_root_name": action.action_root_name,
                    "action_run_time": call.latter,
                    }
                print(data_to_update)
                return data_to_update
            else:
                print("anoj ji")
                print(".....")
                print(call)
                params = [action.application_id, action.add_to_job_id]
                JobAndApplicationDetails = GetStoreProcedureData('GetCandidatesDetails', params)
                candidate_details = JobAndApplicationDetails[0]
                data = {}
                data['candidate'] = action.candidate_id
                data['custom_data'] = call.custom_data
                data['mobile_no'] = candidate_details['mobile_no']
                data['country_code'] = candidate_details['country_code']
                data['bot_status'] = 11
                data['user'] = candidate_details['user_id']
                data['application'] = candidate_details['application_id']
                data['call_to'] = call.call_to
                data['job'] = candidate_details['job_id']
                data['campaign_trigger'] = action.trigger_id
                data['campaign_trigger_history'] = action.id
                # data['is_deleted'] = False
                data['campaign'] = action.campaign_id
                data['campaign_event'] = action.event_id
                data['call_history_id'] = call.call_history_id
                print(data)
                serializer = CallSerializer(data=data)
                if serializer.is_valid():
                    print("call call")
                    serializer.save()
                else:
                    print(serializer.errors)
                print("SEND Call")
                data_to_update = {
                    "action_name": action.action_name,
                    "action_root_name": action.action_root_name,
                    "is_action": True,
                    }
                return data_to_update
        except Calls.DoesNotExist:
            print("event not found")


    def mail(self,action):
        print(f"----------------> mail ---> {action.action_temp_id}")
        event = CampaignEvent.objects.get(id=action.event_id)
        EmailTemplate = EmailTemplates.objects.using('mysqlslave').filter(id=event.email_template_id, is_deleted=False).first()
        if EmailTemplate:
            # params = [action.application_id, action.add_to_job_id]
            params = [action.application_id, action.add_to_job_id,action.id]
            JobAndApplicationDetails = GetStoreProcedureData('GetCandidatesDetailsForCallMessage', params)
            email_subect = prepare_message(JobAndApplicationDetails, EmailTemplate.subject)
            message = prepare_message(JobAndApplicationDetails, EmailTemplate.message)
            message = generate_key(message, JobAndApplicationDetails,'email')
            candidate_details = JobAndApplicationDetails[0]
            current_datetime = datetime.now()
            message_data = {
                'message':message['template'],
                'application': action.application_id,
                'added_by':action.user_id,
                'sms_template_id':EmailTemplate.id,
                'subject': email_subect,
                'sent_date': current_datetime,
                'sended_to': candidate_details['email'],
                'sended_by': EmailTemplate.sended_by,
                'is_otp': 0,
                'campaign_trigger': action.trigger_id,
                'campaign_trigger_history':action.id,
                'campaign': action.campaign_id,
                'campaign_event': action.event_id,

            }
            serializer = EmailLogs_serializer(data=message_data)
            if serializer.is_valid():
                print("Message Email")
                email_instance = serializer.save()
                if message['urlshortner_id']:
                    UrlShortners.objects.filter(id__in=message['urlshortner_id']).update(email_log=email_instance.id)
            else:
                print(serializer.errors)
                print("email error")
            print("SEND Mesage")
            data_to_update = {
                "action_name": action.action_name,
                "action_root_name": action.action_root_name,
                "is_action": True,
                }
            return data_to_update

    def sms(self,action):
        print(f"----------------> SMs ---> {action.action_temp_id}")
        event = CampaignEvent.objects.get(id=action.event_id)
        SmsTemplate = SmsTemplates.objects.using('mysqlslave').filter(id=event.sms_template_id, is_deleted=False).first()
        print(SmsTemplate)
        if SmsTemplate:
            print(f"{action.application_id}, {action.add_to_job_id},{action.id}")
            params = [action.application_id, action.add_to_job_id,action.id]
            JobAndApplicationDetails = GetStoreProcedureData('GetCandidatesDetailsForCallMessage', params)
            message = prepare_message(JobAndApplicationDetails, SmsTemplate.message)
            message = generate_key(message, JobAndApplicationDetails,'sms')
            current_datetime = datetime.now()
            candidate_details = JobAndApplicationDetails[0]
            message_data = {
                'message':message['template'],
                'application': action.application_id,
                'added_by':action.user_id,
                'sms_template_id':SmsTemplate.id,
                'dlt_te_id': SmsTemplate.dlt_te_id,
                'sent_date': current_datetime,
                'sended_to': candidate_details['mobile_no'],
                'sended_by': SmsTemplate.sended_by,
                'is_otp':0,
                'campaign_trigger': action.trigger_id,
                'campaign_trigger_history':action.id,
                'campaign': action.campaign_id,
                'campaign_event': action.event_id,
            }
            serializer = SmsLogs_serializer(data=message_data)
            if serializer.is_valid():
                print("Message Send")
                message_instance = serializer.save()
                if message['urlshortner_id']:
                    UrlShortners.objects.filter(id__in=message['urlshortner_id']).update(sms_log=message_instance.id)

            else:
                print(serializer.errors)
            print("SEND Mesage")
            data_to_update = {
                "action_name": action.action_name,
                "action_root_name": action.action_root_name,
                "is_action": True,
                }
            return data_to_update

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
