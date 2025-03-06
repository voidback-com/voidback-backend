from django.db import models
from .Account import Account



class RoomCategory(models.Model):
    category = models.TextField(max_length=20, blank=True)
    rank = models.BigIntegerField(default=0, blank=True) # category rank across the platform
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category



class EdgeRoomConfig(models.Model):
    # all rooms are public and anyone can join
    admin = models.ForeignKey(Account, on_delete=models.CASCADE)
    default_member_permissions = models.JSONField(blank=False) # the default permissions for joining members
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.admin.username)




class EdgeRoom(models.Model):
    name = models.TextField(max_length=30, blank=False, editable=True)
    description = models.TextField(max_length=2500, blank=True, null=True)
    rank = models.BigIntegerField(default=0, blank=True) # edgeRoom rank amongest other edgeRooms
    categories = models.ManyToManyField(RoomCategory, blank=True)
    config = models.ForeignKey(EdgeRoomConfig, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name



class MemberPermissions(models.Model):

    # Moderator Actions


    # moderates the edge room (any suport moderator can make any user a moderator)
    is_moderator = models.BooleanField(blank=True, default=False)

    # allows the user and other moderators to know why this user's permission was changed
    upated_reason = models.TextField(max_length=3000, blank=True, default="") # reason for the update (a short message by the moderator who updated the user's permissions)

    last_updated = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True) # moderator account etc...
    created_at = models.DateTimeField(auto_now_add=True)

    # can delete posts (if is_super_mod then he can delete mod posts)
    can_delete_posts = models.BooleanField(blank=True, default=False)

    # moderators can remove/add regular members (DEFAULT)
    can_remove_members = models.BooleanField(blank=True, default=False)
    can_remove_moderators = models.BooleanField(blank=True, default=False)
    can_add_moderators = models.BooleanField(blank=True, default=False)


    # Normal Member Actions
    

    # can post, like/dislike and reply in the edge room
    can_post = models.BooleanField(default=True, blank=True)
    can_like = models.BooleanField(default=True, blank=True)
    can_dislike = models.BooleanField(default=True, blank=True)
    can_reply = models.BooleanField(default=True, blank=True)

    # can include an image in posts
    can_post_image = models.BooleanField(default=False, blank=True)

    can_add_members = models.BooleanField(default=True, blank=True) # if the room is private then this normal member can add his friends to the private room




class RoomMembership(models.Model):
    room = models.ForeignKey(EdgeRoom, on_delete=models.CASCADE, null=True, blank=True)
    permissions = models.ForeignKey(MemberPermissions, on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    rank = models.BigIntegerField(default=0, blank=True) # member rank within the edgeRoom
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




