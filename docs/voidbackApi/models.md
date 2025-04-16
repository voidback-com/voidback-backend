
## Models

### **models/Account.py**
> This model file contains all the user and authentication related models

> <a href="../../voidbackApi/models/Account.py">Account.py</a>

<br/>


#### Account(AbstractUser)

> This model inherts from the **AbstractUser** class to customize the default user model and add to it new fields like (**avatar**, **site_link**, etc...)

> you can read more about this: https://docs.djangoproject.com/en/5.1/topics/auth/customizing/



```python

from django_resized import ResizedImageField

avatar = ResizedImageField(size=[320, 320], upload_to="avatars/", force_format="WEBP", null=True, keep_meta=False)

# The avatar is converted into WEBP
# Metadata is removed
# The avatar is resized to a 320x320 image.
```



<br/>

-----

<br/>


#### OneTimePassword(models.Model)
> This is a very simple model that stores generated OTPs in relation to the account model instance.


```python


class OneTimePassword(models.Model):
    otp = models.CharField(max_length=8, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")

    def __str__(self):
        return self.account.username



```



<br/>

-----

<br/>


#### Follow(models.Model)
> This model keeps track of who follows who (when a user clicks the follow button an instance is created where the user is the follower and the following is the account being followed.)

```python


class Follow(models.Model):
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username", related_name="follower")
    following = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username", related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.TextField(blank=True, unique=True) # follower_username:following_username
    # as you can see the hash is unique and is used to prevent duplicate records


    # Example of how the hash is created:
    '''
    {
        "hash": f"{request.user.username}:{username}"
    }
    '''

}

    def __str__(self):
        return self.follower.username

```

<br/>

---


<br/>


### **models/Notifications.py**
> This model file contains a model that stores notifications and a method to create Notification instances.

> <a href="../../voidbackApi/models/Notifications.py.py">Notifications.py</a>

<br/>


```python

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



# This function creates a Notification instance
def newNotification(toUsername: str, fromName: str, navPath: str, body=None, fromAvatar=None, fromNameMessage=None, avatarVerified=False, icon="notificatiton"):
    try:

        account = Account.objects.all().filter(username=toUsername).first()


        if account.full_name == fromName and account.avatar == fromAvatar:
            return

        instance = Notification(account=account, fromAvatar=fromAvatar, avatarVerified=avatarVerified, fromName=fromName, fromNameMessage=fromNameMessage, navPath=navPath, body=body, icon=icon)

        instance.save()

    except Exception:
        return None





```

<br/>

-----




