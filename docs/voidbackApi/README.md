
## Models

### **models/Account.py**
> This model file contains all the user and authentication related models

> <a href="../../voidbackApi/models/Account.py">Account.py</a>

<br/>


==Account(AbstractUser)==
: This model inherts from the **AbstractUser** class to customize the default user model and add to it new fields like (**avatar**, **site_link**, etc...)

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


==OneTimePassword(models.Model)==
: This is a very simple model that stores generated OTPs in relation to the account model instance.


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


==Follow(models.Model)==
: This model keeps track of who follows who (when a user clicks the follow button an instance is created where the user is the follower and the following is the account being followed.)

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



