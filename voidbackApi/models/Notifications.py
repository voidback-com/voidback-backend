from django.db import models
from django.db.transaction import on_commit
from .Account import Account



class Notification(models.Model):
    isRead = models.BooleanField(default=False, blank=True, null=True) # did the account already see this notification

    account = models.ForeignKey(Account, on_delete=models.CASCADE) # the recipient account

    content = models.JSONField(default=[], blank=True) # notification content (json object)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["account", 'isRead', 'created_at'])
        ]




