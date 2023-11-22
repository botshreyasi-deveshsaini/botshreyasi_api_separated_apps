from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connections
from django.utils import timezone
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from candidate.models import CandidateDetails
from application.models import Application, ApplicationDefault
from .models import AddNewJob, Location, InternationalLocations, AddToJob, JobTag, JobUnderRecruiters
from .serializer import AddNewJobSerializer, LocationSerializer, InternationalLocationsSerializer
from helper.views import GetAppID, GetUserID, GetChildWithSelf, GetStoreProcedureData
# Create your views here.


class AddJobView(APIView):
    def post(self, request):  # create New Job
        print(f"Job Details:-->>>>>>>>>>>>>>>>>>>>>>>>{request.data}")
        mutable_data = request.data.copy()
        mutable_data['application'] = GetAppID()
        mutable_data['creater'] = GetUserID()
        serializer = AddNewJobSerializer(data=mutable_data)
        if serializer.is_valid():
            Job = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):  # get Job Details
        application_id = GetAppID()
        jobs = AddNewJob.objects.using('mysqlslave').filter(
            application_id=application_id, is_deleted=False).values()
        print(jobs)
        return Response(jobs)

    def view_assign_job(self, request):
        appid = GetAppID()
        user_id = request.GET.get('managerId')
        isclientdepartment = request.GET.get('isclientdepartment')
        client_department_id = request.Get.get('ClientDepartment')
        if client_department_id is None:
            client_department_id = 0
        child_roles = GetChildWithSelf(appid, user_id)
        print(f"child_roles:-----------------------> {child_roles}")
        if not child_roles:
            child_roles = f"[{user_id}]"
        child_roles = [int(role_id) for role_id in child_roles]

        allid = child_roles
        joined_ids = ','.join(map(str, allid))

        params = [joined_ids, client_department_id, GetAppID()]
        assigned_job = GetStoreProcedureData('getJobAssigned', params)
        return JsonResponse(assigned_job)

    def patch(self, request, job_id):
        application_id = GetAppID()
        job = AddNewJob.objects.filter(
            application=application_id, id=job_id, is_deleted=False).first()
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddNewJobSerializer(job)
        return Response(serializer.data)


class AddToJobView(APIView):
    def post(self, request):
        candidates = request.POST.get('candidates')
        print(f"candidates------------>{candidates}")
        candidates = candidates.split(',')
        print(f"candidates------------>{candidates}")
        job = request.POST.get('job')
        print(f"job------------>{job}")
        if not job:
            return JsonResponse({'msg': 'No Job Selected'}, status=500)
        manager = request.POST.get('manager')
        if not manager:
            manager = GetUserID()

        application = ApplicationDefault.objects.using('mysqlslave').get(application=GetAppID())

        if not application.default_status_id:
            return JsonResponse(['Default Status field is empty. Contact Super Admin.'], status=422)

        alreadyexists = 0
        html = ''
        print(f"candidates-------------------->{candidates}")
        for candidateval in candidates:
            addToJob = AddToJob.objects.filter(
                candidate_id=candidateval, job_id=job).count()

            if addToJob == 0:
                addToJob = AddToJob(
                    candidate_id=candidateval,
                    user_id=manager,
                    job_id=job,
                    status_id=application.default_status_id,
                    ip_address=request.META['REMOTE_ADDR'],
                    application_id=GetAppID(),
                )
                # if jobdata.campaign_id:
                #     addToJob.campaign_status = 'starting'
                #     addToJob.campaign_id = jobdata.campaign_id

                addToJob.save()
            else:
                alreadyexists += 1

            # userself = User.objects.get(id=RoleHelper.GetUserID())
            # is_crm = userself.is_crm

            # if not is_crm:
            #     alreadycalled = ''
            #     callDetail = None
            #     callDetail = Calls.objects.raw('SELECT count(1) as tried FROM calls WHERE job_id=%s AND candidate_id=%s', [job, candidateval])

            #     if callDetail:
            #         alreadycalled = f'(Tried calling {callDetail[0].tried} time(s))'

            #     if jobdata:
            #         job_title = jobdata.job_title
            #     else:
            #         job_title = None

            #     job_title = f'{job_title}{alreadycalled}'

            html = 'job_title'

        return JsonResponse({'alreadyexists': alreadyexists, 'html': html})


class MyJob(APIView):
    def get(self, request):
        print("Manoj's --------> working")
        showalljobs = request.GET.get('showalljobs')
        showrecruiterjobs = request.GET.get('recruterids')
        clientids = request.GET.get('client_id')
        if clientids in ('null', 'undefined', None):
            clientids = 0
        isclientdepartment = request.GET.get('isclientdepartment')
        if not showrecruiterjobs or showrecruiterjobs == 'undefined':
            showrecruiterjobs = GetUserID()

        addnewjobs = []

        if clientids and clientids != "undefined":
            print("manaoj")
            addnewjobs = AddNewJob.objects.filter(
                client_detail_id=clientids,
                application_id=GetAppID(),
                job_status='Active'
            )
        else:
            isvendor = False
            self = "0"

            if isvendor:
                isvendor = 1
                allid = GetUserID()
            else:
                appid = GetAppID()

                # if showalljobs == "0":
                #     allid = GetChildWithSelf(GetAppID(), GetManangerID())
                # else:

                allid = GetChildWithSelf(GetAppID(), GetUserID())

                allid = ','.join(map(str, allid))
                isvendor = 0
                self = showrecruiterjobs
                clientids = clientids

            candidate = request.GET.get('candidate', '')
            candidate = f"%{candidate}%"

            params = [
                allid, isvendor, candidate, self, showalljobs,
                GetAppID(), clientids, isclientdepartment
            ]
            addnewjobs = GetStoreProcedureData('getMyandTeamJobList', params)

        return Response(addnewjobs)


class MyJobCandidates(APIView):
    def get(self, request):
        start_index = int(request.GET.get('startindex', 0))
        end_index = int(request.GET.get('endindex', 20))

        keyword = request.GET.get('keyword', '')
        process = request.GET.get('process', '')
        main_process = request.GET.get('mainprocess', '')
        start_date_str = request.GET.get('start_date', '2020-01-01')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()

        end_date_str = request.GET.get('end_date')
        try:
            if not end_date_str:
                end_date = datetime.now().date() + timedelta(days=1)
            else:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            end_date = datetime.now().date() + timedelta(days=1)

        candidate = request.GET.get('candidate', '')
        selected_jobs = request.GET.get('selectedjob', '')
        is_interview = 9 if request.GET.get('isinterview') else 0
        prm_show_all_detail = request.GET.get('showallcandidate', '')
        location = request.GET.get('location', '')

        all_id = ','.join(map(str, GetChildWithSelf(GetAppID(), GetUserID())))
        if all_id == ',':
            all_id = ''

        param = [all_id, process, selected_jobs, GetUserID(), main_process, GetAppID(), 0, GetUserID(
        ), f'%{candidate}%', is_interview, prm_show_all_detail, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), start_index, end_index]
        print(f"PARAM----------------->{param}")
        data = GetStoreProcedureData(
            'getMyandTeamJobUnderCandidateList', param)
        return Response(data)


class JobTagView(APIView):
    def post(self, request, *args, **kwargs):
        job_tag = JobTag()
        job_tag.user_id = GetUserID()
        job_tag.job_id = request.POST.get('job_id')
        job_tag.ip_address = request.META.get('REMOTE_ADDR')
        job_tag.application_id = GetAppID()
        job_tag.save()

        return JsonResponse({}, status=201)

    def delete(self, request, id, *args, **kwargs):
        job_tag = get_object_or_404(JobTag, application=GetAppID(
        ), job_id=id, is_deleted=False, user_id=GetUserID())
        job_tag.is_deleted = True
        job_tag.save()
        return Response(status=200)


class JobUnderRecruiterListView(APIView):
    def __init__(self, *args, **kwargs):
        self.assigning = kwargs.pop('assigning', True)
        super().__init__(*args, **kwargs)

    def get(self, request):
        job_id = request.GET.get('job_id')
        job_under_recruiters = JobUnderRecruiters.objects.using('mysqlslave').filter(
            job=job_id, is_deleted=False).values()
        return Response(job_under_recruiters)


class AssignjobListView(APIView):
    def post(self, request, *args, **kwargs):
        managers = [value for key, value in request.POST.items()
                    if key.startswith('managers[')]
        jobs = [value for key, value in request.POST.items()
                if key.startswith('jobs[')]
        assignjobdates = request.POST.get('assigndate')
        if assignjobdates == 'OneDay':
            start_date = end_date = timezone.now().date()
        elif assignjobdates == 'TowDay':
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=1)
        else:
            start_date = end_date = None
        print(f"{start_date} and {end_date}")
        # store
        for manager in managers:
            for job in jobs:
                try:
                    job_under_recruiter = JobUnderRecruiters.objects.using(
                        'mysqlslave').filter(user=manager, job_id=job, is_deleted=False)

                    if not job_under_recruiter.exists():
                        job_under_recruiter = JobUnderRecruiters(
                            user_id=manager,
                            job_id=job,
                            is_unassigned=False,
                            ip_address=request.META['REMOTE_ADDR'],
                            application_id=GetAppID(),
                            assign_start=start_date,
                            assign_end=end_date
                        )
                        job_under_recruiter.save()
                except Exception as e:
                    pass
        return JsonResponse({}, status=200)


class UnAssignjobListView(APIView):
    def post(self, request):
        print("working unassignjob")
        if request.method == "POST":
            print("working unassignjob")
            managers = [value for key, value in request.POST.items()
                        if key.startswith('managers[')]
            jobs = [value for key, value in request.POST.items()
                    if key.startswith('jobs[')]
            # store
            for managerval in managers:
                for val in jobs:
                    try:
                        job_under_recruiter = JobUnderRecruiters.objects.using('mysqlslave').get(
                            job_id=val, user_id=managerval, application_id=GetAppID(), is_deleted=False
                        )
                        job_under_recruiter.is_deleted = True  # Set the field to mark as deleted
                        job_under_recruiter.save()
                    except JobUnderRecruiters.DoesNotExist:
                        pass

            return JsonResponse({}, status=200)


class AddJobViewClientDepartment(APIView):
    def get(self, request):
        ClientDepartment = request.GET.get('ClientDepartment')
        application_id = GetAppID()
        jobs = AddNewJob.objects.using('mysqlslave').filter(
            application_id=application_id, department_id=ClientDepartment, is_deleted=False).values()
        print(jobs)

        return Response(jobs)


class JobView(APIView):
    def get(self, request, job_id):
        application_id = GetAppID()
        job = AddNewJob.objects.using('mysqlslave').filter(
            application=application_id, id=job_id, is_deleted=False).first()
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AddNewJobSerializer(job)
        return Response(serializer.data)

class ActivityListView(APIView):
    def patch(self, request, id):
        param = [id, GetAppID()]
        print(f"PARAM----------------->{param}")
        data = GetStoreProcedureData('pr_get_activity_on_jobs', param)
        return Response(data)
    

class LocationCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InternationalLocationCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = InternationalLocations.objects.all()
    serializer_class = InternationalLocationsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetJobTitleSuggestionView(APIView):
    def get(self, request):
        job_title = request.GET.get('job_title')
        query = f"%{job_title}%"
        # return Response(query)
        with connections["mysqlslave"].cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT current_designation FROM candidate_details WHERE LENGTH(current_designation) > 2 AND current_designation LIKE %s LIMIT 10", [query])
            candidate_details = [row[0] for row in cursor.fetchall()]

        return Response(candidate_details)


class SuggestKeySkillsView(View):
    def get(self, request):
        query = request.GET.get('tts', '')
        print(f"query------------->{query}")
        skills = query.split(',')
        skill_filters = [Q(skill_set__icontains=skill) for skill in skills]
        # Combine the Q objects using OR condition
        combined_filter = Q()
        for skill_filter in skill_filters:
            combined_filter |= skill_filter
        results = CandidateDetails.objects.using('mysqlslave').filter(
            combined_filter
        ).values('skill_set')[:1000]
        # with connections["mysqlslave"].cursor() as cursor:
        #     cursor.execute(f"SELECT skill_set FROM candidate_details WHERE skill_set LIKE '%{queryfinal}%' LIMIT 1000;")
        #     results = [row[0] for row in cursor.fetchall()]
        print(f"Result:---------------------> {results}")
        skills = {}
        for result in results:
            result_skills = result['skill_set'].split(',')
            print(f"result_skills:>>>>>>>>>>> {result_skills}")
            for skill in result_skills:
                keyskill = skill.replace("...View More", '').strip().lower()
                if keyskill:
                    if keyskill in skills:
                        skills[keyskill] += 1
                    else:
                        skills[keyskill] = 0
        # Sort the skills dictionary by value in descending order
        skills = dict(sorted(skills.items(), key=lambda x: x[1], reverse=True))
        # Get the top 100 skills
        filteredskills = list(skills.keys())[:100]
        return JsonResponse(filteredskills, safe=False)
