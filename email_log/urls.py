from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #  path('',  views.getHistory.as_view()),
     path('email-templates/',  views.EmailTemplatesListView.as_view()),
     path('email-templates/<int:id>/',  views.EmailTemplatesListView.as_view()),

    #  path('download-excel-format/',views.DownloadExcelFormat.as_view()),
]
