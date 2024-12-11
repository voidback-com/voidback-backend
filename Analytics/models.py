from django.db import models




class Device(models.Model):
    ip = models.TextField()
    country = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    city_metadata = models.JSONField(null=True, blank=True)
    country_metadata = models.JSONField(null=True, blank=True)
    is_mobile = models.BooleanField(default=False, null=True, blank=True)
    is_tablet = models.BooleanField(default=False, null=True, blank=True)
    is_touch_capable = models.BooleanField(default=False, null=True, blank=True)
    is_pc = models.BooleanField(default=False, null=True, blank=True)
    is_bot = models.BooleanField(default=False, null=True, blank=True)
    browser = models.TextField(null=True, blank=True)
    browser_version = models.TextField(null=True, blank=True)
    os = models.TextField(null=True, blank=True)
    os_version = models.TextField(null=True, blank=True)
    device = models.TextField(null=True, blank=True)
    account = models.TextField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        indexes = [
            models.Index(fields=['ip', 'created_at', 'country', 'city', 'country_metadata', 'city_metadata', 'account', 'browser', 'browser_version', 'is_pc', 'is_mobile', 'is_tablet', 'is_bot', 'is_touch_capable', 'device', 'os_version', 'os'])
        ]





class Event(models.Model):
    event_path = models.TextField(blank=True, null=True) # the path in which this event occurred
    event_type = models.TextField(blank=True, null=True) 

    data = models.JSONField(blank=True, null=True) # extra info on the nature of the event

    created_at = models.DateTimeField(auto_now_add=True)

    account = models.TextField(default="anonymous", blank=True, null=True) # account username
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['event_path', 'event_type', 'account', 'created_at', 'device'])
        ]



# instance is created everytime we look at the user's activity in the analytics page
class UsersActivityHistory(models.Model):
    data = models.JSONField()
    hash = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        indexes = [
            models.Index(fields=['data', "hash", "created_at"])
        ]



