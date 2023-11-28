from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HiringManagersSerializer

from helper.views import GetAppID

from .models import HiringManagers

# Create your views here.


class View1(APIView):

    def post(self, request):

        data = request.data.copy()

        serializer = HiringManagersSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        data = HiringManagers.objects.filter(is_deleted=False).values()

        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            hiringManager = HiringManagers.objects.get(id=id)
        except HiringManagers.DoesNotExist:
            return Response({'error': 'hiring_manager does not exist'}, status=status.HTTP_404_NOT_FOUND)

        application_id = GetAppID()
        mutable_data = request.data.copy()
        mutable_data['application_id'] = application_id

        print(mutable_data['off_days'], type(mutable_data['off_days']))

        serializer = HiringManagersSerializer(hiringManager, data=mutable_data)

        # return Response(data=mutable_data, status=200)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: Recheck if this is meant by patch
    def patch(self, request, id):
        application_id = GetAppID()
        print(application_id, id)
        hiringManager = HiringManagers.objects.filter(id=id, is_deleted=False).first()

        if hiringManager:
            serializer = HiringManagersSerializer(hiringManager)
            return Response(serializer.data)
        else:
            return Response(data={"result": "data not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):

        print(request, id)
        try:
            hiringManager = HiringManagers.objects.get(id=id)
        except HiringManagers.DoesNotExist:
            return Response({'error': 'hiring manager does not exist'}, status=status.HTTP_404_NOT_FOUND)

        print(hiringManager.is_deleted)
        hiringManager.is_deleted = True
        hiringManager.save()
        return Response(data={'status': 'deleted'})
