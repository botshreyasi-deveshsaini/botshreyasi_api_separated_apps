from django.urls import path
from . import views

urlpatterns = [
    path('insert/',views.INSERT_MESSAGE_TEMPLATE.as_view()),
    path('getdata/',views.GET_MESSAGE_TEMPLATE.as_view()),
    path('delete_data/',views.DELETE_MESSAGE_TEMPLATE.as_view()),
    path('update_data/',views.UPDATE_MESSAGE_TEMPLATE.as_view()),
    
]
