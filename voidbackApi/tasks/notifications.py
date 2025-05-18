import json
import asyncio
from ..models.Notifications import Notification



def create_notification(user, content: dict):
    Notification.objects.create(account=user, content=content) # create new notification


