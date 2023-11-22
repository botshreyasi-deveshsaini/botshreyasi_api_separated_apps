from django.urls import path
from . import views

urlpatterns = [

    path('create-job/',  views.AddJobView.as_view()),
    path('view-jobs/',  views.AddJobView.as_view(), name='jobs-list-get'),
    path('view-assign-job/',  views.AddJobView.as_view(), name='view_assign_job'),
    path('show-job/<int:job_id>/',
         views.AddJobView.as_view(), name='jobs-list-get'),
    path('add-to-job/',  views.AddToJobView.as_view()),
    path('job-list/', views.MyJob.as_view()),
    path('candidates/',views.MyJobCandidates.as_view()),
    path('client-department/',  views.AddJobViewClientDepartment.as_view(),
         name='jobs-list-get-using-client-department'),
    path('job-tag/',  views.JobTagView.as_view(), name='jobs-tag'),
    path('job-tag/<int:id>/',  views.JobTagView.as_view(), name='delete'),
    path('job-under-recruiters/', views.JobUnderRecruiterListView.as_view(),
         name='job_under_recruiter_list'),
    path('assign-job/', views.AssignjobListView.as_view(),
         name='assignJob'),
    path('unassign-job/', views.UnAssignjobListView.as_view(),
         name='unassignjob'),
         
    path('activity/<int:id>/',  views.ActivityListView.as_view(), name='get'),

    path('location/',  views.LocationCreateView.as_view()),
    path('international-location/',
         views.InternationalLocationCreateView.as_view()),
    path('jobtitle-suggestion/',  views.GetJobTitleSuggestionView.as_view()),
    path('suggest-key-skills/',  views.SuggestKeySkillsView.as_view()),


]
