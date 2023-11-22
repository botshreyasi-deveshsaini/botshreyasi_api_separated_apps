from django.urls import path
from . import views

urlpatterns = [
    path('add-department/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('list-department/', views.DepartmentListCreateView.as_view(), name='department-list-get'),
    path('list-client/', views.ClientListCreateView.as_view(), name='client-list-get'),
    path('list-client/<int:id>/',  views.ClientListCreateViewSingle.as_view()),

    # path('<int:pk>/', views.DepartmentRetrieveUpdateView.as_view(), name='department-retrieve-update'),

]