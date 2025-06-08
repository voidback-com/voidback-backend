"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
django_asgi_app = get_asgi_application()


from voidbackApi.routing import websocket_urlpatterns


patterns = websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "https": django_asgi_app,
    # (we can add other protocols under http)
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(patterns))
    )
})

