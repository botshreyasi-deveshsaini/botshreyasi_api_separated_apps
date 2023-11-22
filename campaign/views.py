from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from .models import Campaign, CampaignEvent, CampaignChannel
from .serializers import CampaignEventSerializer,CampaignSerializer,CampaignEventSerializerCall
from helper.views import GetAppID, GetUserID, GetQueryData

# Create your views here.


class CampaignCreateViewList(APIView):
    def post(self, request):
        print(request.data)
        ip_address = request.META.get('REMOTE_ADDR')
        campaign = {
            'user':GetUserID(),
            'application':GetAppID(),
            'campaign_name':request.data.get('campaign_name'),
            'campaign_description':request.data.get('description'),
            'is_published':bool(request.data.get('Published')),
            'ip_address':ip_address
        }
        # campaign.save()
        # serialized_campaign = serializers.serialize('json', [campaign])
        serializer = CampaignSerializer(data=campaign)
        serializer.is_valid(raise_exception=True)
        Campaign = serializer.save()
        return Response(serializer.data)

    def get(self, request):
        print(f"Campaign--------->{request.GET}")
        start_index = int(request.GET.get('startindex', 0))
        end_index = int(request.GET.get('endindex', 20))
        application_id = GetAppID()
        user_id = GetUserID()
        data = GetQueryData(
            f"select * from campaigns ce where user_id={user_id} and application_id={application_id} order by id asc limit {start_index}, {end_index}")
        return Response(data)


class CampaignEventCreateViewList(APIView):
    def get(self, request):
        campaign_id = request.GET.get('id')
        application_id = GetAppID()
        user_id = GetUserID()
        data = GetQueryData(
            f"select ce.*, ce.event_name as name, cc.channel_root_name from campaign_events ce left join campaign_channels cc on cc.id= ce.channel_id where ce.campaign_id={campaign_id} and ce.user_id={user_id} and ce.application_id={application_id} and ce.is_deleted=0 order by ce.id asc")
        return Response(data)

    def post(self, request):
        application_id = GetAppID()
        user_id = GetUserID()
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        mutable_data['user'] = user_id
        mutable_data['parent'] = request.data.get('parent_id')
        mutable_data['channel'] = request.data.get('channel_id')
        mutable_data['candidate_status'] = request.data.get(
            'candidate_status_id')
        mutable_data['campaign'] = request.data.get('campaign_id')
        print(f"Campaign mutable_data -------> {mutable_data}")
        serializer = CampaignEventSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, event_id):
        print(f"Campaign Events ->> {request},   event_id ====> {event_id}")
        try:
            campaign_event = CampaignEvent.objects.get(id=event_id)
        except CampaignEvent.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        application_id = GetAppID()
        user_id = GetUserID()
        mutable_data = request.data.copy()
        mutable_data['parent'] = request.data.get('parent_id')
        mutable_data['channel'] = request.data.get('channel_id')
        mutable_data['candidate_status'] = request.data.get(
            'candidate_status_id')
        mutable_data['campaign'] = request.data.get('campaign_id')
        print(f"Campaign update mutable_data -------> {mutable_data}")

        mutable_data['application'] = application_id
        mutable_data['user'] = user_id

        serializer = CampaignEventSerializer(campaign_event, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = CampaignEvent.objects.all()
    serializer_class = CampaignEventSerializer

    # @action(detail=True, methods=['delete'])
    def delete(self, request, event_id=None):
        try:
            campaign_event = CampaignEvent.objects.get(id=event_id)
        except CampaignEvent.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        campaign_event.is_deleted = True
        campaign_event.save()
        return Response({'status': 'soft-deleted'})


class CampaignChannelCreateViewList(APIView):
    def get(self, request):
        campaignchannel = CampaignChannel.objects.using('mysqlslave').values()
        return Response(campaignchannel)


class CampaignGetCall(APIView):
    def get(self, request):
        campaign_id = request.GET.get('campaign_id')
        print(campaign_id)
        application_id = GetAppID()
        campaignchannel = CampaignChannel.objects.using('mysqlslave').filter(channel_root_name = 'call').first()
        print(f"campaign_chann-------> {campaignchannel.id}")
        campaignCalls = CampaignEvent.objects.using('mysqlslave').filter(campaign=campaign_id,channel=campaignchannel.id, application=application_id)
        serializer = CampaignEventSerializerCall(campaignCalls, many=True)
        return Response(serializer.data)
