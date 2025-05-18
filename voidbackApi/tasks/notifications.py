from channels.layers import get_channel_layer
import asyncio
from ..models.Notifications import Notification



def create_notification(user, content: dict):
    Notification.objects.create(account=user, content=content) # create new notification

    channel_layer = get_channel_layer()

    unread = Notification.objects.filter(account=user, isRead=False).count()

    asyncio.run(channel_layer.group_send(
        f"notifications-{user.id}", # room name
        {
            'count': unread,
        }
    ))


