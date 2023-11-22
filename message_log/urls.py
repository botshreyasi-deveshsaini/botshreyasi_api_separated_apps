from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('sms-templates/',  views.SmsTemplatesListView.as_view()),
    path('sms-templates/<int:id>/',  views.SmsTemplatesListView.as_view()),

]
