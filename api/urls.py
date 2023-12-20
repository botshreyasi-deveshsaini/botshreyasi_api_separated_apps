"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls import handler404

from application.views import handle_not_found

urlpatterns = [
    # path('send-email/', include('emailconfig.urls')),



    # path('admin/', admin.site.urls),
    # path('user/', include('userprofile.urls')),
    path('api/', include('authorization.urls')),
    # path('mypermission/', include('rolepermission.urls')),
    # path('master/', include('master.urls')),
    # path('candidate/', include('candidate.urls')),
    # path('department/', include('departments.urls')),
    # path('tracker/', include('tracker.urls')),
    # path('job/', include('jobs.urls')),
    # path('candidate-status/', include('candidate_status.urls')),
    # path('smtp/', include('smtpdetail.urls')),
    # # path('message-template/', include('message_tempelate.urls')),
    # path('bot/', include('bot.urls')),
    # path('call/', include('call.urls')),
    # path('chat/', include('chat.urls')),

    # path('campaign/', include('campaign.urls')),
    # path('campaign-trigger/', include('campaign_trigger.urls')),

    # path('sms/', include('message_log.urls')),
    # path('email/', include('email_log.urls')),


    # # path('authenticate/', jwt_views.TokenObtainPairView.as_view(),
    # #      name='token_obtain_pair'),
    # # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
    # #      name='token_refresh'),    path('', include('tracker.urls')),
    # path('dashboard/', include('dashboard.urls')),
    # path('history/', include('history.urls')),

    # path('hiring-manager/', include('hiring_manager.urls')),
    # path('permissions/', include('rolepermission.urls')),
    
]
