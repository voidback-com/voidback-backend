from django.db import models
from .Account import Account



# a user made report
class Report(models.Model):
    object_type = models.TextField()
    object_id = models.BigIntegerField(blank=True, null=True)
    object_uuid = models.TextField(blank=True, null=True)
    description = models.TextField()
    reporter = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, to_field="username", related_name="reporter")
    priority = models.IntegerField()
    disturbance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username", related_name="resolved_by", null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['resolved', 'object_type', 'object_id', 'disturbance', 'priority', 'created_at', 'resolved_by'])
        ]


    def __str__(self):
        if self.resolved:
            return f"{self.object_type} [RESOLVED] [{self.resolved_by.username}]"
        else:
            return self.object_type
