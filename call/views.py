from django.shortcuts import render
from rest_framework.views import APIView
from bot.models import BotDetails
from candidate.models import CandidateDetails
from helper.views import *
from .serializers import CallSerializer
from jobs.models import AddNewJob
import json
from django.db.models import Q
import logging
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CallLogListView(APIView):
    def get(self, request):
        print(request.GET.get('end_index'))
        start_index =int(request.GET.get('start_index', '0'))
        end_index =int(request.GET.get('end_index', '20'))
        print(request.GET.get('end_index'))
        print(end_index)

        app_id = GetAppID()
        user_id = GetUserID()
        child_roles = GetChildWithSelf(app_id, user_id)
        allid = child_roles
        joined_ids = ','.join(map(str, allid))
        params = [app_id, user_id, joined_ids, start_index, end_index]
        print(params)
        call_log = GetStoreProcedureData(
            'GetCallLogsWithCandidate', params)
        return Response(call_log)


class CallLogChildsListView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if id is None:
            return Response(error="Id not found")
        start_index =int(request.GET.get('start_index', '0'))
        end_index =int(request.GET.get('end_index', '20'))
        app_id = GetAppID()
        user_id = GetUserID()
        child_roles = GetChildWithSelf(app_id, user_id)
        allid = child_roles
        joined_ids = ','.join(map(str, allid))
        params = [1, 10]
        params = [id, app_id, user_id, joined_ids, start_index, end_index]
        call_log = GetStoreProcedureData(
            'GetCallLogsWithChilds', params)
        # call_log = GetStoreProcedureData(
        #     'GetCallLogsWithTotalCountAndFilter', params)
        return Response(call_log)


class PrePareToCall(APIView):
    def post(self, request):
        print("Calls------------------------------>")
        # print(request.POST.get('candidates'))

        # candidates_id = request.POST.get('candidates')
        job_id = request.POST.get('job')
        # call_manager = request.POST.get('manager')
        # call_type = request.POST.get('inbound_lead')
        # language_code = request.POST.get('language')
        # job_location = request.POST.get('job_location')
        clientdepartment_id = request.POST.get('department_id')
        # array_string = ','.join(candidates_id)
        mutable_data = request.data.copy()
        mutable_data['application'] = 1  # GetAppID()
        Botdetail = BotDetails.objects.using(
            'mysqlslave').filter(id=1, is_deleted=False).first()
        custom_data = CreateCustomData(Botdetail.custom_data, mutable_data)
        app_id = GetAppID()
        params = [app_id, job_id, clientdepartment_id]
        print(params)
        JobAndApplicationDetails = GetStoreProcedureData(
            'GetJobAndApplicationDetails', params)
        custom_data = CreateCustomData(
            custom_data, JobAndApplicationDetails[0])
        return SendCall(mutable_data, custom_data)
        print("Call Sended")


def SendCall(data, custom_data):
    print("call sended")
    candidates_id = data['candidates']
    candidates_id = candidates_id.split(',')
    print(f"array_string------------->{candidates_id}")
    for candidate in candidates_id:
        print(f"candidate---------->{candidate}")
        CandidateDetail = CandidateDetails.objects.using(
            'mysqlslave').filter(id=candidate, is_deleted=False).first()
        try:
            model_fields = CandidateDetails._meta.get_fields()
            row_name = CandidateDetails._meta.verbose_name
            CandidateDetailWithRowColumn = MysqlCombineModelsRowColumn(
                row_name, model_fields, CandidateDetail)
            print(f"merged_data---------->{CandidateDetailWithRowColumn}")
            custom_data = CreateCustomData(
                custom_data, CandidateDetailWithRowColumn)
            data['candidate'] = candidate
            data['custom_data'] = json.loads(json.loads(custom_data))
            # print(json.loads(json.loads(custom_data)))
            data['mobile_no'] = CandidateDetailWithRowColumn['mobile_no']
            data['country_code'] = CandidateDetailWithRowColumn['country_code']
            data['call_initiate_id'] = 1
            data['user'] = data['manager']
            serializer = CallSerializer(data=data)
            if serializer.is_valid():
                candidate = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error('Error in dilate return:: ' + str(e))
            print(e)
            pass

        print("sending")


def CreateCustomData(custom_data, datas):
    custom_data = custom_data
    custom_data = json.dumps(custom_data)
    custom_data = StrReplace(custom_data, datas)
    return custom_data


class GetCallDetails(APIView):
    def get(self, request):
        client_id = request.GET.get('clientId')
        is_vendor = 0
        if client_id is not None:
            add_new_jobs = AddNewJob.objects.filter(
                client_detail_id=client_id,
                app_id=GetAppID(),
                job_status='Active'
            )
        else:
            # is_vendor = RoleHelper.IsVendor()
            # self = "0"
    
            # if is_vendor:
            #     is_vendor = 1
            # all_id = GetUserID()
            # else:
            app_id = GetAppID()
            user_id = GetUserID()
            child_roles = GetChildWithSelf(app_id, user_id)
            allid = child_roles
            all_id = ','.join(map(str, allid))
            is_vendor = 0
            self = GetUserID()
    
            candidate = request.GET.get('candidate', '')
            candidate = f"%{candidate}%"
    
            start_date = request.GET.get('start_date', '2000-01-01')
            start_date = start_date.split('T')[0]
    
            end_date = request.GET.get('end_date', '')
            if end_date:
                end_date = end_date.split('T')[0]
            else:
                end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
            client_ids = request.GET.get('client_id', 0)
    
            is_client_department = request.GET.get('isclientdepartment')
# $param = array('data' => $allid, 'isvendor' => $isvendor, 'candidate' => $candidate, 'self' => $self, 'app_id' => RoleHelper::GetAppID(), 'end_date' => $end_date, 'start_date' => $start_date, 'client_id' => $clientids, 'isclientdepartment' => $isclientdepartment); //
            param = [all_id, is_vendor, candidate, self,app_id,end_date,start_date,client_id,is_client_department]
            call_log = GetStoreProcedureData('getMyandTeamJobListByCallHistory', param)
            return Response(call_log)
        # Perform further operations with the obtained data
        # Return the results as JsonResponse or render a template

    
    
class CandidateINCalls(APIView):
    def get(sel,request):
        app_id = GetAppID()
        callsource = request.GET.get('callsource')
        candidate_calltype = request.GET.get('calltype')
        selectedjobs = request.GET.get('selectedjob')
        startindex = request.GET.get('startindex')
        endindex = request.GET.get('endindex')
    
        if startindex is None or startindex == 'undefined':
            startindex = 0
    
        if endindex is None or endindex == 'undefined':
            endindex = 20
    
        if selectedjobs is None or selectedjobs == ',':
            selectedjobs = ''
    
        Education = request.GET.get('Education')
        if Education is None or Education == "undefined" or Education == 'null':
            Education = 0
    
        relocatelocation = request.GET.get('relocatelocation')
        if relocatelocation is None or relocatelocation == "undefined" or relocatelocation == 'null':
            relocatelocation = 0
    
        jobOpportunity = request.GET.get('jobOpportunity')
        if jobOpportunity is None or jobOpportunity == "undefined" or jobOpportunity == 'null':
            jobOpportunity = 0
    
        nightshift = request.GET.get('nightshift')
        if nightshift is None or nightshift == "undefined" or nightshift == 'null':
            nightshift = 0
    
        isinternet = request.GET.get('isinternet')
        if isinternet is None or isinternet == "undefined" or isinternet == 'null':
            isinternet = 0
    
        Concentrixpremises = request.GET.get('Concentrixpremises')
        if Concentrixpremises is None or Concentrixpremises == "undefined" or Concentrixpremises == 'null':
            Concentrixpremises = 0
    
        issystem = request.GET.get('issystem')
        if issystem is None or issystem == "undefined" or issystem == 'null':
            issystem = 0
    
        Diplomaflanguage = request.GET.get('Diplomaflanguage')
        if Diplomaflanguage is None or Diplomaflanguage == "undefined" or Diplomaflanguage == 'null':
            Diplomaflanguage = 0
    
        Workedinpast = request.GET.get('Workedinpast')
        if Workedinpast is None or Workedinpast == "undefined" or Workedinpast == 'null':
            Workedinpast = 0
    
        # if candidate_calltype is None or candidate_calltype == "undefined" or candidate_calltype == 'null':
        #     call_port = AddNewJob.objects.get(id=selectedjobs)
        #     candidate_calltype = call_port.calltype
    
        keyword = request.GET.get('keyword')
        filterdropdown = request.GET.get('filterdropdown')
        process = request.GET.get('process')
        mainprocess = 0
        searchcandidatetext = request.GET.get('searchcandidatetext')
        candidate = request.GET.get('candidate')
    
        if candidate is None:
            candidate = ''
    
        isinterview = 9
        if request.GET.get('isinterview') is not None:
            isinterview = request.GET.get('isinterview')
    
        toexp = request.GET.get('Experienceto')
        if toexp == 'undefined' or toexp is None:
            toexp = 50
    
        fromexp = request.GET.get('Experiencefrom')
        if fromexp == 'undefined' or fromexp is None:
            fromexp = 88
    
        tosalary = request.GET.get('salaryto')
        if tosalary == 'undefined' or tosalary is None:
            tosalary = 90
    
        fromsalary = request.GET.get('salaryfrom')
    
        if fromsalary == 'undefined' or fromsalary is None:
            fromsalary = 0
    
        default_location = request.GET.get('location')
    
        Average = request.GET.get('Average')
        if Average is None or Average == 'undefined':
            Average = 0
    
        firstskill = request.GET.get('firstskill')
        if firstskill is None or firstskill == 'undefined':
            firstskill = 0
    
        secondskill = request.GET.get('secondskill')
        if secondskill is None or secondskill == 'undefined':
            secondskill = 0
    
        thirdskill = request.GET.get('thirdskill')
        if thirdskill is None or thirdskill == 'undefined':
            thirdskill = 0
    
        Grammar = request.GET.get('grammar')
        if Grammar is None or Grammar == 'undefined':
            Grammar = 0
    
        SecGrammar = request.GET.get('secgrammar')
        if SecGrammar is None or SecGrammar == 'undefined':
            SecGrammar = 0
    
        noticp = request.GET.get('noticp')
        if noticp is None or noticp == 'undefined':
            noticp = '0'
    
        if keyword:
            candidatedetails = CandidateDetails.objects.filter(application_id=GetAppID(), candidate_name__contains=keyword)
        else:
            candidatedetails = CandidateDetails.objects.filter(application_id=GetAppID())
    
        allid = ''
        isvendor = 0
        vendorId = 0
    

        allid = GetChildWithSelf(GetAppID(), GetUserID())
    
        allid = ','.join(map(str, allid))
        if allid == ',':
            allid = ''
    
        start_date = request.GET.get('start_date')
    
        if start_date is not None:
            start_date = start_date.split('T')[0]
        else:
            start_date = '2000-01-01'
    
        end_date = request.GET.get('end_date')
    
        if end_date is not None:
            end_date = end_date.split('T')[0]
        else:
            end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    
        candidate_status = request.GET.get('candidatestatus')
    
        if candidate_status is None or candidate_status == 'undefined':
            candidate_status = 'all'

    
        # Construct your 'param' dictionary with all the parameters
        param = [
            allid,
            process,
            selectedjobs,
            GetUserID(),
            int(mainprocess),
            app_id,
            isvendor,
            vendorId,
            candidate,
            isinterview,
            start_date,
            end_date,
            toexp,
            fromexp,
            tosalary,
            fromsalary,
            default_location,
            Average,
            firstskill,
            secondskill,
            thirdskill,
            noticp,
            candidate_calltype,
            Grammar,
            SecGrammar,
            Education,
            relocatelocation,
            jobOpportunity,
            nightshift,
            isinternet,
            Concentrixpremises,
            issystem,
            Diplomaflanguage,
            Workedinpast,
            startindex,
            endindex,
            candidate_status
            ]    
        print(param)
        candidate_in_call = GetStoreProcedureData('getCandidatebyCallsDetail', param)
        return Response(candidate_in_call)
        # Use these 'param' and 'param115' dictionaries to perform your database query
    
        
    