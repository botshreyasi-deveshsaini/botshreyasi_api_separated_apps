from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HiringManagersSerializer

from helper.views import GetAppID, GetUserID, GetStoreProcedureData

from .models import HiringManagers

# Create your views here.

DB_PROCEDURE__GET_HIRING_MANAGER_WITH_TOTAL_COUNT = "get_hiring_manager_with_total_count"


class View1(APIView):

    def post(self, request):
        print(request.POST)
        data = request.data.copy()

        application_id = GetAppID()
        user_id = GetUserID()

        data['application_id'] = application_id
        data['user_id'] = user_id

        off_days = []
        for key, value in request.POST.items():
                if key.startswith('off_days[') and key.endswith(']'):
                    off_days.append(int(value))
        print(off_days)

        off_days = "[" + ",".join(map(str, off_days)) + "]"

        data['off_days'] = off_days

        print(off_days)
        # off_days_ids = [int(request.POST.get(f'off_days[{i}]')) for i in range(len(request.POST.getlist('off_days')))]#request.POST.getlist('off_days')
        # permission_ids = request.data.get('off_days[0]')
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(off_days)


        serializer = HiringManagersSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        # Consider for global variables/constants.
        STARTINDEX = 0
        ENDINDEX = 20

        startindex = STARTINDEX
        endindex = ENDINDEX

        try:
            startindex = int(request.GET.get('startindex'))
            endindex = int(request.GET.get('endindex'))

        except TypeError:
            pass

        params = [startindex, endindex]

        # WARNING: this is found to be slow. try doing it in better way if possible.
        # maybe use django queries itself? or optimize procedure queries.
        # Or avoid querying the database for total_count if possible
        data = GetStoreProcedureData(DB_PROCEDURE__GET_HIRING_MANAGER_WITH_TOTAL_COUNT,
                                     params=params)

        return Response(data=data, status=status.HTTP_200_OK)

    # def get(self, request):

    #     try:
    #         startindex = int(request.GET.get('startindex'))
    #         endindex = int(request.GET.get('endindex')) + 1

    #         data = HiringManagers.objects.filter(is_deleted=False)[startindex:endindex].values()

    #     except:
    #         data = HiringManagers.objects.filter(is_deleted=False).values()

    #     return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            hiringManager = HiringManagers.objects.get(id=id)
        except HiringManagers.DoesNotExist:
            return Response({'error': 'hiring_manager does not exist'}, status=status.HTTP_404_NOT_FOUND)

        application_id = GetAppID()
        user_id = GetUserID()
        mutable_data = request.data.copy()
        mutable_data['application_id'] = application_id
        mutable_data['user_id'] = user_id

        # print(mutable_data['off_days'], type(mutable_data['off_days']))

        off_days = []
        for key, value in request.POST.items():
                if key.startswith('off_days[') and key.endswith(']'):
                    off_days.append(int(value))
        print(off_days)

        off_days = "[" + ",".join(map(str, off_days)) + "]"
        mutable_data['off_days'] = off_days

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


class View2(APIView):

    pass
