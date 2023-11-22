from django.shortcuts import render
from rest_framework.views import APIView
from .models import CandidateDetails
from history.models import History
from .serializers import CandidateSerializer
from helper.views import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import requests
import re
from django.db.models import Q
import os
import mysql.connector
from tracker.views import TrackerFormat
from helper.views import GetQueryData
from django.db import connections, connection
conn = connections["mysqlslave"]
cursor = connections["mysqlslave"].cursor()

main_path = os.path.dirname(os.path.abspath(__file__))

# Create your views here.


class CandidateListCreateViewHistory(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # queryset = CandidateDetails.objects.all()
        print("Manoj ------------------> start")

        application_id = GetAppID()
        user_id = GetUserID()
        source_id = request.data.get('source_id')
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')
        mutable_data['email'] = email
        mutable_data['mobile_no'] = mobile_no
        mutable_data['mobile_no'] = mobile_no
        mutable_data['source'] = source_id

        print(f"Manoj ------------------> {mutable_data}")
        candidate_exists = CandidateDetails.objects.filter(
    (Q(email=email) | Q(mobile_no=mobile_no)), application=application_id
)
        # (
        #     CandidateDetails.objects.filter(email=email, application=application_id).exists() or
        #     CandidateDetails.objects.filter(
        #         mobile_no=mobile_no, application=application_id).exists()
        # )
        print("Candidates queryset:", candidate_exists)  # Debugging line

        if candidate_exists.exists():
            print("Candidate already exist  store history")
            if candidate_exists.count() == 1:    
                candidate = candidate_exists.first()
                serializer = CandidateSerializer(candidate, data=mutable_data)
                if serializer.is_valid():
                    candidate = serializer.save()
                history_entry = History.objects.create(
                    candidate=candidate, user_id=user_id, source_id=source_id, application_id = application_id)
                return Response("Candidate Added", status=status.HTTP_201_CREATED)
            elif candidate_exists.count() > 1:
                return Response(
                    {'error': 'Multiple candidates with the same email or mobile number exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            print("Candidate Storing -->")
            serializer = CandidateSerializer(data=mutable_data)
            if serializer.is_valid():
                candidate = serializer.save()
                history_entry = History.objects.create(
                    candidate=candidate, user_id=user_id, source_id=source_id, application_id = application_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateListCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # queryset = CandidateDetails.objects.all()
        print("Manoj ------------------> start")

        application_id = GetAppID()
        user_id = GetUserID()
        source_id = request.data.get('source_id')
        mutable_data = request.data.copy()
        mutable_data['application'] = application_id
        email = request.data.get('email')
        mobile_no = request.data.get('mobile_no')
        mutable_data['email'] = email
        mutable_data['mobile_no'] = mobile_no
        mutable_data['mobile_no'] = mobile_no
        mutable_data['source'] = source_id

        print("Manoj ------------------> {mutable_data}")
        candidate_exists = (
            CandidateDetails.objects.filter(email=email, application=application_id).exists() or
            CandidateDetails.objects.filter(
                mobile_no=mobile_no, application=application_id).exists()
        )
        if candidate_exists:
            print("Candidate already exist  store history")
            candidate = CandidateDetails.objects.get(
                email=email, application=application_id)
            # Check if the candidate exists
            history_entry = History.objects.create(
                candidate=candidate, user_id=user_id, source_id=source_id)
            return Response("Candidate Added", status=status.HTTP_201_CREATED)
        else:
            print("Candidate Storing -->")
            serializer = CandidateSerializer(data=mutable_data)
            if serializer.is_valid():
                candidate = serializer.save()
                history_entry = History.objects.create(
                    candidate=candidate, user_id=user_id, source_id=source_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                uploaded_file = request.FILES['file']
                file_path = os.path.join(f'{main_path}/store_excel/', uploaded_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                excel_file_path =  f"{main_path}/store_excel/{uploaded_file.name}"
                application_id = GetAppID()
                print(f"application_id---------->{application_id}")
                user_id = GetUserID()
                print(f"user_id---------->{user_id}")
                source_id = request.data.get('source_id')
                print(f"source_id---------->{source_id}")
                trackerId = request.data.get('trackerno')
                print(f"trackerId---------->{trackerId}")
                uploaded_file = request.FILES['file']
                df1 = pd.read_excel(excel_file_path)

                # application_id = 1  # GetAppID()
                # user_id = 9  # GetUserID()
                # source_id = 1  # request.data.get('source_id')
                # parameters = json.loads(request.body)
                # print(parameters)
                # trackerId = parameters['trackerno']
                # df1 = parameters['upload_file']
                # print(df1)
                # df1 = pd.DataFrame(df1)
                # print(f"df1--------->{df1}")
                get_tracker = f"select * from trackers where id={trackerId};"
                trackers_data = GetQueryData(get_tracker)
                tracker_instance = TrackerFormat()
                tc = tracker_instance.tracker_value_db(trackers_data)

                tracker_master = [i for i in tc.keys()]
                col_db = []
                col_cand = []
                for i in tracker_master:
                    if tc[f"{i}"] != "NULL":
                        col_db.append(tc[f"{i}"])
                        col_cand.append(i)
                db_value = {}
                for i in col_cand:
                    db_value[tc[f"{i}"]] = [i for i in df1[f"{i}"]]

                r = len([j for j in df1[f"{col_cand[0]}"]])
                message_upload = ""
                for i in range(r):
                    candidate_dict = {}
                    for j in col_db:
                        if j == "mobile_no":
                            number = db_value[f"{j}"][i]
                            if isinstance(number, str):
                                # Remove non-numeric characters
                                cleaned_number = re.sub(r'\D', '', number)
                                if cleaned_number.startswith('91'):
                                    cleaned_number = cleaned_number[2:]
                                if len(cleaned_number) >= 10:
                                    # Take the last 10 digits
                                    normalized_numbers = cleaned_number[-10:]
                                    candidate_dict[f"{j}"] = normalized_numbers
                            elif isinstance(number, int):
                                normalized_numbers = str(number)[-10:]
                                candidate_dict[f"{j}"] = normalized_numbers
                        else:
                            candidate_dict[f"{j}"] = db_value[f"{j}"][i]
                    candidate_dict['application'] = application_id
                    email = candidate_dict['email']
                    mobile_no = candidate_dict['mobile_no']
                    try:
                        candidate_exists = (
                            CandidateDetails.objects.filter(email=email, application=application_id).exists() or
                            CandidateDetails.objects.filter(
                                mobile_no=mobile_no, application=application_id).exists()
                        )
                        if candidate_exists:
                            print("Candidate already exists added history")
                            candidate = CandidateDetails.objects.get(
                                email=email, application=application_id)
                            history_entry = History.objects.create(
                                candidate=candidate, user_id=user_id, source_id=source_id)
                            message_upload = "Candidate Added"
                        else:
                            print("Candidate does not exist added All")
                            serializer = CandidateSerializer(
                                data=candidate_dict)
                            if serializer.is_valid():
                                candidate = serializer.save()
                                history_entry = History.objects.create(
                                    candidate=candidate, user_id=user_id, source_id=source_id)
                                message_upload = "Candidate Added"
                            else:
                                message_upload = f"Invalid data for candidate: {candidate_dict}"
                    except Exception as e:
                        print(f"Exception-----------> {e}")
                if r == 0:
                    message_upload = 'Oops Your Excel Is Empty!'
                    return Response(message_upload)

        except Exception as e:
            return Response(e)



class Candidates(APIView):
    def patch(self,request,candidate_id):
        application_id = GetAppID()
        user_id = GetUserID()
        candidate = CandidateDetails.objects.get(
            id=candidate_id, application_id=application_id)
        # return Response(tracker.serialize())
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)