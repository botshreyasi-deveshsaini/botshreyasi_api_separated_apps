from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from helper.views import *
import json
from django.db import connection
from django.http import JsonResponse
from django.db import connections, connection

from tracker.views import TrackerFormat
import pandas as pd
import requests
import re
import os

conn = connections["mysqlslave"]
cursor = connections["mysqlslave"].cursor()
main_path = os.path.dirname(os.path.abspath(__file__))


@method_decorator(csrf_exempt, name='dispatch')
class getHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        print(":---------------------------->")
        recruiterid = str(request.GET.get('recruiter'))
        start_date = str(request.GET.get('start_date'))
        end_date = str(request.GET.get('end_date'))
        key = str(request.GET.get('key'))

        startindex = str(request.GET.get('startindex'))
        if startindex == 'null' or startindex is None or startindex == 'undefined':
            startindex=0

        endindex = str(request.GET.get('endindex'))
        if endindex == 'null' or endindex is None or endindex == 'undefined':
            endindex=20            

        if recruiterid == 'null' or recruiterid == 'undefined':
            recruiterid = GetUserID()

        if key == 'null' or key is None or key == 'undefined':
            key = ''

        print(key, '::::::::::::', key == 'null')
        key = f'%{key}%'
        params = [recruiterid, GetAppID(), start_date, end_date, key, startindex, endindex]
        print(params)
        candidateDetailsHistory = GetStoreProcedureData('GetHistory', params)
        return JsonResponse(candidateDetailsHistory, safe=False)


class AddCandidate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(':::::::::')
        print('POST', request.POST)

        print('======>', type(request.POST))

        print("===============")
        # print('BODY', request.body)
        print('''''''''''''''''''''''')
        print('JSON', json.loads(request.body.decode('utf-8')))
        print("////////////////")
        return Response('historyquery')


class DownloadExcelFormat(APIView):
    def post(self, request, *args, **kwargs,):
        if request.method == "POST":
            # parameters = json.loads(request.body)
            # trackerId = parameters["trackerno"]

            trackerId = request.data.get("trackerno")

            # parameters = request.data.copy()

            # print(f"parameters:------->{parameters}")
            qry1 = "select * from candidate_details;"
            cursor.execute(qry1)
            result = cursor.fetchall()
            result2 = [column[0] for column in cursor.description]

            list1 = []
            dict2 = {}
            for j in result:
                for i in range(len(result2)):
                    dict2[f"{result2[i]}"] = j[i]
                list1.append(dict2)
                dict2 = {}
            list1 = []
            print("================================")
            print(list1, trackerId)
            tracker_instance = TrackerFormat()
            filename = tracker_instance.get_data(list1, trackerId)
        return Response(filename)
