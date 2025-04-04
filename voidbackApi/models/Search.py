from datetime import timezone
from django.db import models
import uuid, pathlib
from .Account import Account


class SearchQuery(models.Model):
    query = models.TextField(unique=True)
    rank = models.BigIntegerField(default=1)
    object_name = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.query

