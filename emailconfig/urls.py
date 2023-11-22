from django.urls import path
from . import views

urlpatterns = [
    path('send-mail/',views.SendMail.as_view()),
    path('mail-track/',views.EmailTracker.as_view()),
]
