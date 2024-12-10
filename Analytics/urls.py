from django.urls import path
from .views import (
    logEvent,
)





urlpatterns = [

    # ANALYTICS
    path("logEvent", logEvent),

]
