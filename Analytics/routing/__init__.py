from django.urls import re_path
from Analytics.consumers.NegativeEvents import NegativeEventsConsumer
from Analytics.consumers.NeutralEvents import NeutralEventsConsumer
from Analytics.consumers.UsersActivity import UsersActivityConsumer
from Analytics.consumers.PositiveEvents import PositiveEventsConsumer



websocket_analytics_urlpatterns = [
    re_path(r"analytics/usersActivity", UsersActivityConsumer.as_asgi()),
    re_path(r"analytics/positiveEvents", PositiveEventsConsumer.as_asgi()),
    re_path(r"analytics/negativeEvents", NegativeEventsConsumer.as_asgi()),
    re_path(r"analytics/neutralEvents", NeutralEventsConsumer.as_asgi()),
]
