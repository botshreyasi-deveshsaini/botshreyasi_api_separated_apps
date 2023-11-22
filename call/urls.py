from django.urls import path
from . import views

urlpatterns = [
    path('send-call-ats/', views.PrePareToCall.as_view(), name='callSend'),
    path('call-log/', views.CallLogListView.as_view(), name='callLog'),
    path('call-log-childs/', views.CallLogChildsListView.as_view(),
         name='callLogChilds'),
    path('joblistbycallhistory/',views.GetCallDetails.as_view()),
    path('callcandidatesdetailhistory/',views.CandidateINCalls.as_view())
]
