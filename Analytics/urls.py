from django.urls import path
from .views import (
    logEvent,
    eventsOverview
)





urlpatterns = [

    # ANALYTICS
    path("logEvent", logEvent),
    path("eventsOverview", eventsOverview)

]
