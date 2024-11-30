from django.urls import re_path
from ..consumers.Notifications import NotificationsCountConsumer


websocket_urlpatterns = [
    re_path(r"notifications/count", NotificationsCountConsumer.as_asgi())
]
