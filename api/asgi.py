"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from django.urls import path
# from RESUME_PARSER import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from RESUME_PARSERCHANNELS import routing as r1
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()
# websocket_urlpatterns =[
#     path('resumeparser/', consumers.Resumesocket.as_asgi())
# ]

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            r1.websocket_urlpatterns
            )
    )
})

