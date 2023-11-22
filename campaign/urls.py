from django.urls import path
from . import views
from . import campaign_config
urlpatterns = [
    path('campaign/',  views.CampaignCreateViewList.as_view()),
   
    path('flow/',  views.CampaignEventCreateViewList.as_view()),
    path('flow/<int:event_id>/',  views.CampaignEventCreateViewList.as_view()),
    
    path('channel/',  views.CampaignChannelCreateViewList.as_view()),
    path('get-call/', views.CampaignGetCall.as_view()),
    path('run-events/',  campaign_config.RunCampaign.as_view()),
    

]
