from rest_framework.views import APIView
from rest_framework.response import Response
from helper.views import GetStoreProcedureData, CalculateDatetimeInterval
from datetime import datetime


class RunCampaign(APIView):
    def get(self, request):
        current_datetime = datetime.now()
        print("working-------campaign config")
        CandidatesInCampaign = GetStoreProcedureData('GetCandidateinCampaign', [])
        for candidate in CandidatesInCampaign:
            application_id = candidate.get('application_id')
            campaign_id = candidate.get('campaign_id')
            event_id = candidate.get('campaign_event_id')
            campaign_status = candidate.get('campaign_status')
            campaign_run_time = candidate.get('campaign_run_time')
            candidate_status_id = candidate.get('status_id')
            params = [application_id, campaign_id, event_id, 0]
            if current_datetime > campaign_run_time:
                CampaignsData = GetStoreProcedureData(
                    'GetCampaignEventsToRunCampaign', params)
                for events in CampaignsData:
                    print(f"event -------> {events}")
                    if events.get('event_type') == 'condition':
                        if events.get('candidate_status_id') == candidate_status_id:
                            actionparam = [application_id, campaign_id, 0, events.get('id')]
                            NextCampaignAction = GetStoreProcedureData(
                                'GetCampaignEventsToRunCampaign', actionparam)
                            ''' find date '''
                            CreateActionDate = self.find_date(
                                NextCampaignAction)
                            print(
                                f'CreateActionDate ---------->{CreateActionDate}')
                    elif events.get('event_type') == 'action':
                        print("action")

        return Response(f'all Done at {current_datetime}')

    # def find_date(self, actions_Campaign):
    #     current_datetime = datetime.now()
    #     action_times_and_ids = []
    #     for nextaction in actions_Campaign:
    #         if nextaction.get('trigger_mode') == 'immediate':
    #             id = nextaction.get('id')
    #             action_time = current_datetime
    #             print(action_time)
    #         elif nextaction.get('trigger_mode') == 'interval':
    #             id = nextaction.get('id')
    #             action_time = CalculateDatetimeInterval(nextaction.get(
    #                 'trigger_interval'), nextaction.get('trigger_interval_unit'))
    #             print(action_time)
    #         elif nextaction.get('trigger_mode') == 'date':
    #             id = nextaction.get('id')
    #             action_time = nextaction.get(
    #                 'trigger_date')
    #         print(nextaction.get('trigger_mode'))
    #         action_times_and_ids.append((action_time, id))
    #         print(action_times_and_ids)
    #     return action_times_and_ids

    def find_date(self, actions_Campaign):
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

            # Append action_time to the dictionary
            nextaction['action_time'] = action_time

        # Sort the actions_Campaign list based on the 'action_time' key in ascending order
        actions_Campaign.sort(key=lambda x: x['action_time'])

        return actions_Campaign
