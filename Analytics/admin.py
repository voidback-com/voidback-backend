from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, Device


@admin.register(Event)
class EventAdmin(ModelAdmin):
    search_fields = ['id', "object_type"]
    sortable_by = ['id']



@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    search_fields = ["ip"]
    sortable_by = ['id']


