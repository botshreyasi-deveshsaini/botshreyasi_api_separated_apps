from django.urls import path
from . import views

urlpatterns = [
    path('relations/',  views.CandidateStatusRelations.as_view()),
    path('relations/<int:id>',  views.CandidateStatusRelations.as_view()),
]