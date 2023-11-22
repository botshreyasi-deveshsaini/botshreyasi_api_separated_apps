from django.urls import path
from . import views

urlpatterns = [
    path('chat-bot/',views.ChatBot.as_view()),
]
