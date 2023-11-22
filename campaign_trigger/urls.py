from django.urls import path
from . import views
from .import update_data
urlpatterns = [
    path('start-campaign/',  views.CampaignStart.as_view(),name='start-campaign'),
    path('start-action/',  views.TriggerAction.as_view(),name='start-action'),
    path('next-action/' , views.CreateNewAction.as_view()),
    path('update-campaign-status/',update_data.UpdateData.as_view())

]
