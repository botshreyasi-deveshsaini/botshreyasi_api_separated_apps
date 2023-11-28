from django.urls import path
from . import views

urlpatterns = [
    path('relations/',  views.CandidateStatusRelations.as_view()),
    path('relations/<int:id>',  views.CandidateStatusRelations.as_view()),

    path('candidate-status/', views.CandidateStatus2.as_view()),
    path('candidate-status-relations/', views.CandidateStatusRelations2.as_view()),
    path('candidate-details/', views.CandidateDetails.as_view()),
]
