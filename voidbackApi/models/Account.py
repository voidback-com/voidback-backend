from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import pathlib

from django.utils.crypto import secrets


def generateOTP():
    return secrets.token_hex(4)



class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.CharField(max_length=320, blank=False, unique=True)
    username = models.CharField(max_length=25, blank=False, unique=True)
    full_name = models.CharField(max_length=128, blank=False, unique=False)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(max_length=1024, blank=True)
    site_link = models.TextField(max_length=130, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isVerified = models.BooleanField(default=False, null=True, blank=True)
    rank = models.BigIntegerField(default=0, blank=True)


    USERNAME_FIELD = "email"


    REQUIRED_FIELDS = ["username", "full_name"]


    def __str__(self):
        return self.username

    class Meta:
        app_label = "voidbackApi"



class OneTimePassword(models.Model):
    otp = models.CharField(max_length=8, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")

    def __str__(self):
        return self.account.username






class Follow(models.Model):
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username", related_name="follower")
    following = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username", related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.TextField(blank=True, unique=True) # username:post_id


    def __str__(self):
        return self.follower.username



class AccountActiveStatus(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account.username




