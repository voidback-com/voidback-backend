from django.urls import path
from .views import gfetch


urlpatterns = [
    path("", gfetch),
]
