from django.urls import re_path
from Analytics.consumers.UsersActivity import UsersActivityConsumer



websocket_analytics_urlpatterns = [
    re_path(r"analytics/usersActivity", UsersActivityConsumer.as_asgi())
]
