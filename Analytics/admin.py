from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, Device, UsersActivityHistory


@admin.register(Event)
class EventAdmin(ModelAdmin):
    search_fields = ['id', "object_type"]
    sortable_by = ['id']



@admin.register(Device)
class DeviceAdmin(ModelAdmin):
    search_fields = ["ip"]
    sortable_by = ['id']




@admin.register(UsersActivityHistory)
class UsersActivityHistoryAdmin(ModelAdmin):
    search_fields = ["hash"]
    sortable_by = ['id']


