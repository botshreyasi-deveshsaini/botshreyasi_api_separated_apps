from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
         path('',  views.getPermission.as_view()),
         path('create-areas/', views.AreaRegistrationView.as_view(), name='Area register'),
         path('update-areas/<int:pk>/', views.AreaUpdateView.as_view(), name='Area Update'),
         path('create-permission/', views.PermissionView.as_view(), name='Permission register'),
         path('create-rolepermission/', views.RolePermissionView.as_view(), name='Permission register'),

]