from django.urls import path
from . import views
urlpatterns=[
    path('bot-details/',views.BotListCreateView.as_view(),name='bot-list-create')
]