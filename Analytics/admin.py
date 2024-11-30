from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event


@admin.register(Event)
class EventAdmin(ModelAdmin):
    search_fields = ['id', "object_type", "event_tone"]
    sortable_by = ['id']


