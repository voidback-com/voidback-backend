from django.db import models



    

# finger print allows tracking behavior of one user (authenticated or not)
class Fingerprint(models.Model):
    username = models.TextField()
    email = models.TextField() # all
    addresses = models.JSONField(default=[]) # all the ip addresses belonging to this user
    userAgents = models.JSONField(default=[]) # all the user agents belonging to this user
    locations = models.JSONField(default=[])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        indexes = [
            models.Index(fields=['username', 'email', 'created_at', 'updated_at'])
        ]


# tribes's are a collection of similar fingerprints each finger print must belong to a tribe
class Tribe(models.Model):
    # this allows us to track a group of people with similar behaviors
    members = models.ManyToManyField(Fingerprint, related_name="members")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        indexes = [
            models.Index(fields=['created_at', 'updated_at'])
        ]





class Event(models.Model):
    event_path = models.TextField(blank=True, null=True) # the path in which this event occurred
    event_type = models.TextField(blank=True, null=True) # click, etc...

    data = models.JSONField(blank=True, null=True) # extra info on the nature of the event

    created_at = models.DateTimeField(auto_now_add=True)

    account = models.TextField(default="anonymous", blank=True, null=True) # account username
    fingerprint = models.ForeignKey(Fingerprint, on_delete=models.DO_NOTHING, null=True)


    class Meta:
        indexes = [
            models.Index(fields=['event_path', 'event_type', 'account', 'created_at', 'fingerprint'])
        ]





