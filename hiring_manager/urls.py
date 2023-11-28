from django.urls import path
from . import views

urlpatterns = [
    path("", views.View1.as_view()),
    path("<int:id>/", views.View1.as_view()),
]