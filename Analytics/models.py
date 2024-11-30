from django.db import models



class Event(models.Model):
    event_path = models.TextField(blank=True, null=True) # the path in which this event occurred
    event_type = models.TextField(blank=True, null=True) # click, etc...

    data = models.JSONField(blank=True, null=True) # extra info on the nature of the event

    created_at = models.DateTimeField(auto_now_add=True)

    account = models.TextField(default="anonymous", blank=True, null=True) # account username



    class Meta:
        indexes = [
            models.Index(fields=['event_path', 'event_type', 'account', 'created_at'])
        ]





