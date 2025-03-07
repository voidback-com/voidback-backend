from django.urls import re_path
from ..consumers.Notifications import NotificationsCountConsumer
from ..consumers.DirectMessage import LiveDirectMessageConsumer


websocket_urlpatterns = [
    re_path(r"notifications/count", NotificationsCountConsumer.as_asgi()),
    re_path(r"dms", LiveDirectMessageConsumer.as_asgi())
]
