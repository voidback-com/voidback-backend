
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




### **models/Platform.py**
> This model file contains two models **PlatformMessage** which stores platform related messages and **PlatformMessageImpression** which stores user impressions (essentially used to check if the user has seen the latest platform message if not it will display it).

> <a href="../../voidbackApi/models/Platform.py">Platform.py</a>


```python


# a platform message example: "We just updated our terms of service and privacy policy"
class PlatformMessage(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True) # optional image
    title = models.TextField() # the title the of the platform message
    description = models.TextField() # details
    created_at = models.DateTimeField(auto_now_add=True) # self-explanatory


    # links example: [{"label": "contact us", "link": "/contact/us", "isInternal": true}]
    links = models.JSONField(blank=True, null=True) 
    # links = array(object(label: str, link: str, isInternal: bool))


    author = models.ForeignKey(Account, on_delete=models.CASCADE) # self-explanatory

    class Meta:
        indexes = [
            models.Index(fields=["title", 'author', 'created_at', 'description'])
        ]

  
    def __str__(self):
        return self.title




class PlatformMessageImpression(models.Model): # if an instance exists that means the account has seen the message so no need to display it on the frontend!
    message = models.ForeignKey(PlatformMessage, on_delete=models.DO_NOTHING, blank=True, null=True) # the id of the platform message
    account = models.ForeignKey(Account, on_delete=models.CASCADE) # the id of the account instance
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["message", "account", "created_at"])
        ]


    def __str__(self):
        return str(self.pk)




```

<br/>


### **models/ReportManagement.py**
> This model file contains one model **Report** which stores reports on a given object: (Account, WriteUp, Comment, etc...)


> <a href="../../voidbackApi/models/ReportManagement.py">ReportManagement.py</a>


```python

# a user made report
class Report(models.Model):
    object_type = models.TextField() # Account, WriteUp, Comment ....
    object_id = models.BigIntegerField(blank=True, null=True) # Comment.id, WriteUp.id, ...
    object_uuid = models.TextField(blank=True, null=True) # Account.id because Account.id is a uuid
    description = models.TextField() # user description of the reported object
    reporter = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, to_field="username", related_name="reporter")
    priority = models.IntegerField() # report's priority (0-100)
    disturbance = models.IntegerField() # report's disturbance (0-100)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False) # is the report resolved?
    resolved_at = models.DateTimeField(blank=True, null=True) # when was this report resolved?
    resolved_by = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username", related_name="resolved_by", null=True, blank=True) # who resolved this report? (ideally a staff member with certain permissions)


    class Meta:
        indexes = [
            models.Index(fields=['resolved', 'object_type', 'object_id', 'disturbance', 'priority', 'created_at', 'resolved_by'])
        ]


    def __str__(self):
        if self.resolved:
            return f"{self.object_type} [RESOLVED] [{self.resolved_by.username}]"
        else:
 
```



<br/>


### **models/Search.py**
> This model file contains one model **SearchQuery** which stores queries on a given object: (WriteUp, Account, etc...)


> <a href="../../voidbackApi/models/Search.py">Search.py</a>


```python


class SearchQuery(models.Model):
    query = models.TextField(unique=True) # the search query
    rank = models.BigIntegerField(default=1) # how many times this exact search query was repeated
    object_name = models.TextField(default="") # object_name -> (WriteUp, Account, ...)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.query

```




<br/>


### **models/Writeup.py**
> This model file contains a bunch of models related to the actual write ups on voidback.


> <a href="../../voidbackApi/models/Search.py">Search.py</a>



```python

# The thumbnail you see in the write up cards
class WriteUpThumbnail(models.Model):
    thumbnail = ResizedImageField(size=[700, 500], upload_to="thumbnails/", force_format="WEBP", keep_meta=False, scale=1, quality=100)

    def __str__(self):
        return str(self.pk)




# the tags you see under the searchbar
class Tag(models.Model):
    tag = models.TextField(max_length=30, blank=False, null=False, unique=True)
    rank = models.BigIntegerField(default=0, blank=True) # number of writeups using this tag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.tag


    class Meta:
        indexes = [
            models.Index(fields=['tag', "rank", 'created_at',  "updated_at"])
        ]



# a series is essentially a folder that contains a bunch of write ups (kinda like a playlist)
class Series(models.Model):
    name = models.TextField() # the name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True) # the author

    class Meta:
        indexes = [
            models.Index(fields=["name", 'created_at',  "updated_at"])
        ]




# This is the actual write up model
class WriteUp(models.Model):
    title = models.TextField() # the title you see in the card
    content = models.JSONField() # the tiptap editor json content
    thumbnail = models.ForeignKey(WriteUpThumbnail, blank=True, on_delete=models.CASCADE, null=True) # the tumbnail
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True) # a many to many relationship with Tag
    author = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username") # author of the writeup
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rank = models.BigIntegerField(default=0, blank=True, null=True) # incremented everytime the writeup is viewed (when the user clicks on the write up card)
    edited = models.BooleanField(default=False, blank=True) # whether this write up is edited or not
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, blank=True, null=True) # series (optional) the series that contains this writeup


    def __str__(self):
        return str(self.pk)


    class Meta:
        indexes = [
            models.Index(fields=["author", "title", "series", "edited", "rank", 'created_at', "updated_at"])
        ]




# this model stores the Likes and Views of a given write up
class WriteUpImpression(models.Model):
    writeup = models.ForeignKey(WriteUp, on_delete=models.CASCADE, to_field="id", related_name="writeup")
    impression = models.IntegerField(default=0, blank=True, editable=True) # (0 = view), (1 = view and like)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    hash = models.TextField(blank=True, unique=True) # username:writeup_id
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.pk)


    class Meta:
        indexes = [
            models.Index(fields=['writeup', 'account', 'impression', "hash", 'created_at', "updated_at"])
        ]




# this model represents the very simple foryou algorithm behind voidback
class ForYou(models.Model):
    series = models.JSONField(default=[]) # series that contain write ups you liked
    authors = models.JSONField(default=[]) # authors of write ups you liked
    tags = models.JSONField(default=[]) # tags used by write ups you liked (used to look for related write ups)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        indexes = [
            models.Index(fields=['account', 'series', 'tags', 'authors', 'created_at', "updated_at"])
        ]


    def __str__(self):
        return self.account.username



 

# The comment model
class Comment(models.Model):
    writeup = models.ForeignKey(WriteUp, on_delete=models.CASCADE) # the write up this comment is under
    author = models.ForeignKey(Account, on_delete=models.CASCADE) # the author of the comment
    comment = models.TextField() # the actual comment
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comment_parent", null=True, blank=True) # parent comment (optional) (when a comment has a parent the comment is a reply to that parent comment)
    rank = models.BigIntegerField(default=0, blank=True)


    def __str__(self):
        return self.comment



    class Meta:
        indexes = [
            models.Index(fields=['rank', 'comment', 'writeup', 'author', 'created_at'])
        ]




# Comment Impressions (an instance is created when you like a comment and the impression is set to zero when you unlike the comment)
class CommentImpression(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field="id", related_name="comment_impression")
    impression = models.IntegerField(default=1, blank=True, editable=True) # (0 = unliked (previously liked), 1 = like)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    hash = models.TextField(blank=True, unique=True) # username:writeup_id
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.pk)


    class Meta:
        indexes = [
            models.Index(fields=['comment', 'account', 'impression', "hash", 'created_at', "updated_at"])
        ]



```

