from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
         path('profile/',  views.getProfile.as_view()),
         path('myteam/',  views.getTeam.as_view()),

]