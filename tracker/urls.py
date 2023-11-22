from django.urls import path
from . import views

urlpatterns = [
    # path("tracker/", views.Format.as_view()),
    # path("tracker-master/", views.Format.as_view()),
    path('tracker-master/', views.TrackerMasterView.as_view(), name='tracker-master-list-create'),
    path('tracker-master/<int:tracker_id>/', views.TrackerMasterView.as_view(), name='tracker-master-retrieve-update-destroy'),

    path('tracker/', views.TrackerView.as_view(), name='tracker-list-create'),

]