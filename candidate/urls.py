from django.urls import path
from . import views

urlpatterns = [
    path('add-candidate/', views.CandidateListCreateViewHistory.as_view(), name='candidate-list-create'),
    path('Excel-candidate/', views.CandidateListCreateView.as_view(), name='candidate-list-create-excel'),
    path('candidate/<int:candidate_id>/', views.Candidates.as_view(),  name='candidate'),
]
