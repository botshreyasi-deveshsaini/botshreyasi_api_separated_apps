from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
         path('gender/',  views.getGender.as_view()),
         path('industries/', views.IndustryCreateView.as_view(), name='industry-create'),
         path('functional-areas/', views.FunctionalAreaCreateView.as_view(), name='functional-area-create'),

]