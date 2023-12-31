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
         path('create-user-role/', views.RoleRegistrationView.as_view()),
         path('update-permissions/', views.UpdatePermissions.as_view(), name="Permissions Update"),
         path('permissions-areas-view/', views.PermissionsAreasView.as_view()),
         path('role-permissions-permissions-view/', views.RolePermissions_Permissions_View.as_view())

]