from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rich import print
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, connections
from django.shortcuts import render
from django.core.exceptions import ValidationError

import pandas as pd
import requests
import re
import os
import numpy as np
import json
import mysql.connector

from .models import TrackerMaster, Tracker
from .serializers import TrackerMasterSerializer, TrackerSerializer
from helper.views import GetAppID, GetUserID, GetQueryData

# conn = mysql.connector.connect(
#    user='testdb@bilateral-dev-testingdb', password='Qj5N2~f7', database='bot',  auth_plugin='mysql_native_password')
conn = connections["mysqlslave"]
cursor = connection.cursor()

main_path = os.path.dirname(os.path.abspath(__file__))


class TrackerMasterListCreateView(APIView):
    def post(self, request):
        print("Tracker Master")


class TrackerView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        tracker_name = request.data.get('tracker_name')
        tracker_data = request.data.get('tracker_data')
        print(
            f"tracker_name---------------------> {tracker_name} \n tracker_data->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{tracker_data}")

        if not tracker_name or not tracker_data:
            return Response({'message': 'Missing required fields'}, status=400)

        try:
            data = json.loads(tracker_data)
        except json.JSONDecodeError:
            return Response({'message': 'Invalid JSON data'}, status=400)

        # data['tracker_name'] = tracker_name
        # data['tracker_name'] = tracker_name
        application = GetAppID()
        user_id = GetUserID()
        data = request.data.copy()
        data['application'] = application
        data['created_by'] = user_id
        print(f"data<<<<<<<>>>>>>>>>>>>>>>>>>{data}")
        serializer = TrackerSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'message': str(e)}, status=400)

        application = GetAppID()
        tracker_exists = Tracker.objects.filter(
            application=application, tracker_name=tracker_name).exists()
        print(f"data<<<<<<<>>>>>>>>>>>>>>>>>>{data}")
        print(f"data<<<<<<<>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<data")

        if tracker_exists:
            return Response({'message': 'This tracker already exists. Please change the tracker name.'}, status=422)

        serializer.save()
        return Response({'success': True})

    def get(self, request):
        application_id = GetAppID()
        trackers = Tracker.objects.filter(
            application_id=application_id, is_deleted=False)
        serializer = TrackerSerializer(trackers, many=True)
        return Response(serializer.data)


class TrackerMasterView(APIView):
    def post(self, request):
        application_id = GetAppID()
        user_id = GetUserID()
        data = request.data.copy()
        data['application'] = application_id
        data['created_by'] = user_id
        serializer = TrackerMasterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=400)

    def get(self, request):
        application_id = GetAppID()
        trackers = TrackerMaster.objects.filter(
            application_id=application_id, is_deleted=False)
        serializer = TrackerMasterSerializer(trackers, many=True)
        return Response(serializer.data)
    def patch(self, request, tracker_id):
        application_id = GetAppID()
        user_id = GetUserID()
        tracker = TrackerMaster.objects.get(
            id=tracker_id, application_id=application_id)
        # return Response(tracker.serialize())
        serializer = TrackerMasterSerializer(tracker)
        return Response(serializer.data)
    
    def put(self, request, tracker_id):
        application_id = GetAppID()
        user_id = GetUserID()
        tracker = TrackerMaster.objects.get(
            id=tracker_id, application_id=application_id)
        data = request.data.copy()
        data['application'] = application_id
        data['created_by'] = user_id

        serializer = TrackerMasterSerializer(tracker, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, tracker_id):
        print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
        application_id = GetAppID()
        tracker = TrackerMaster.objects.get(
            id=tracker_id, application_id=application_id)
        tracker.is_deleted = True
        tracker.save()
        return Response({'success': True})

# class TrackerMasterListCreateView(generics.ListCreateAPIView):
#     # queryset = TrackerMaster.objects.filter(is_deleted=False)
#     # serializer_class = TrackerMasterSerializer


# class TrackerMasterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TrackerMaster.objects.filter(is_deleted=False)
#     serializer_class = TrackerMasterSerializer


class TrackerFormat:
    def fetch_data_from_sql(self, candidate, tracker):
        try:
            cursor.execute(candidate)
            candidate_records = cursor.fetchall()
            candidate_column = [column[0] for column in cursor.description]
            cursor.execute(tracker)
            tracker_records = cursor.fetchall()
            tracker_column = [column[0] for column in cursor.description]

            candidate_information = []
            for i in candidate_records:
                candidate_information.append(dict(zip(candidate_column, i)))

            tracker_information = []
            for i in tracker_records:
                tracker_information.append(dict(zip(tracker_column, i)))
            print(tracker_information, candidate_information)
            return tracker_information, candidate_information
        except:
            conn.rollback()

    def clean(self, string):
        string = string.replace("{", "")
        string = string.replace("}", "")
        return string

    def tracker_value_db(self, trackers_data):
        for i in trackers_data:
            id = i['id']
            clean_i = self.clean(i['tracker_data'])
            clean_i = [j.split(":")[1] for j in clean_i.split(", ")]
            dicts = {}
            for j in clean_i:
                DB_queary = f"select * from tracker_masters where id={int(j)};"
                DB_Fields = GetQueryData(DB_queary)
                for k in DB_Fields:
                    if k['id'] == int(j):
                        dicts[k['display_name']] = k['db_name']
                        print(dicts)
        return dicts

    def get_data(self, data, trackerId):
        get_tracker = f"select * from trackers where id={trackerId};"
        trackers_data = GetQueryData(get_tracker)
        trackers_datas = self.tracker_value_db(trackers_data)
        excel_header = [i for i in trackers_datas.keys()]
        filename = "manoj1234"
        excel_str = {}
        for i in excel_header:
            excel_str[f"{i}"] = []
        print(".......... dict2")
        print(excel_str)
        print(".......... dict2")
        if len(data) != 0:
            for i in data:
                for j in range(len(excel_header)):
                    excel_str[f"{excel_header[j]}"].append(i[f"{trackers_datas[excel_header[j]]}"])
        new = pd.DataFrame.from_dict(excel_str)
        new.to_excel(os.path.join(
            main_path, f"FORMAT_DOWNLOAD/{filename}.xlsx"), index=False)

        # if len(data) == 0:
        #     data2 = self.createtable(trackers_datas)
        #     data2.to_frame().T.to_excel(os.path.join(
        #         main_path, f"FORMAT_DOWNLOAD/{filename}.xlsx"), index=False)
        return os.path.join(main_path, f"FORMAT_DOWNLOAD/{filename}.xlsx")
