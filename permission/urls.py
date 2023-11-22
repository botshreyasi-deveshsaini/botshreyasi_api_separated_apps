# urls.py
from django.urls import path
from .views import (
    AreaListCreateView, AreaRetrieveUpdateDestroyView,
    PermissionListCreateView, PermissionRetrieveUpdateDestroyView,
    UserRoleListCreateView, UserRoleRetrieveUpdateDestroyView,
    RolePermissionListCreateView, RolePermissionRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('areas/', AreaListCreateView.as_view(), name='area-list-create'),
    path('areas/<int:pk>/', AreaRetrieveUpdateDestroyView.as_view(), name='area-retrieve-update-destroy'),
    path('permissions/', PermissionListCreateView.as_view(), name='permission-list-create'),
    path('permissions/<int:pk>/', PermissionRetrieveUpdateDestroyView.as_view(), name='permission-retrieve-update-destroy'),
    path('user-roles/', UserRoleListCreateView.as_view(), name='user-role-list-create'),
    path('user-roles/<int:pk>/', UserRoleRetrieveUpdateDestroyView.as_view(), name='user-role-retrieve-update-destroy'),
    # path('users/', UserListCreateView.as_view(), name='user-list-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('role-permissions/', RolePermissionListCreateView.as_view(), name='role-permission-list-create'),
    path('role-permissions/<int:pk>/', RolePermissionRetrieveUpdateDestroyView.as_view(), name='role-permission-retrieve-update-destroy'),
]
