from django.db import models
from django.db.transaction import on_commit
from .Account import Account


class Notification(models.Model):
    # did the account already see this notification
    isRead = models.BooleanField(default=False, blank=True, null=True)

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE)  # the recipient account

    # notification content (json object)
    content = models.JSONField(default=[], blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["account", 'isRead', 'created_at'])
        ]
