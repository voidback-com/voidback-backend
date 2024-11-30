from django.db import models
from django.db.transaction import on_commit
from .Account import Account
from .Post import Post



class Notification(models.Model):
    isRead = models.BooleanField(default=False, blank=True, null=True) # did the account already see this notification
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username") # the recipient account
    fromAvatar = models.TextField(blank=True, null=True) # url of the from avatar: displayed in the card header on the left
    avatarVerified = models.BooleanField(default=False, blank=True, null=True)
    fromNameMessage = models.TextField(blank=True, null=True) # message in the same line as fromName with a space in between them (not bold)
    fromName = models.TextField() # under the fromAvatar (fromName is bold)
    body = models.TextField(blank=True, null=True) # text in the bottom of the card
    navPath = models.TextField(null=True, blank=True) # the path the card will navigate to when clicked
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.TextField(default="notification", blank=True)


    class Meta:
        indexes = [
            models.Index(fields=["account", 'isRead', 'created_at'])
        ]




def newNotification(account: Account, fromName: str, navPath: str, body=None, fromAvatar=None, fromNameMessage=None, avatarVerified=False, icon="notificatiton"):
    try:

        if account.full_name == fromName and account.avatar == fromAvatar:
            return

        instance = Notification(account=account, fromAvatar=fromAvatar, avatarVerified=avatarVerified, fromName=fromName, fromNameMessage=fromNameMessage, navPath=navPath, body=body, icon=icon)

        instance.save()

    except Exception:
        return None


