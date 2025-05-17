from datetime import timezone
from django.db import models
from .Account import Account
from django_resized import ResizedImageField





class WriteUpThumbnail(models.Model):
    thumbnail = ResizedImageField(size=[1600, 900], upload_to="thumbnails/", force_format="WEBP", keep_meta=False, scale=1, quality=100)

    def __str__(self):
        return str(self.pk)




class Tag(models.Model):
    tag = models.TextField(max_length=30, blank=False, null=False, unique=True)
    rank = models.BigIntegerField(default=0, blank=True) # number of posts using this tag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.tag


    class Meta:
        indexes = [
            models.Index(fields=['tag', "rank", 'created_at',  "updated_at"])
        ]



class Series(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["name", 'created_at',  "updated_at"])
        ]




class WriteUp(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    thumbnail = models.ForeignKey(WriteUpThumbnail, blank=True, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False, blank=True)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, blank=True, null=True) # series (optional)


    def __str__(self):
        return str(self.pk)


    class Meta:
        indexes = [
            models.Index(fields=["author", "title", "series", "edited", 'created_at', "updated_at"])
        ]




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




class ForYou(models.Model):
    series = models.JSONField(default=[])
    authors = models.JSONField(default=[])
    tags = models.JSONField(default=[])
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        indexes = [
            models.Index(fields=['account', 'series', 'tags', 'authors', 'created_at', "updated_at"])
        ]


    def __str__(self):
        return self.account.username



 

class Comment(models.Model):
    writeup = models.ForeignKey(WriteUp, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comment_parent", null=True, blank=True)
    rank = models.BigIntegerField(default=0, blank=True)


    def __str__(self):
        return self.comment



    class Meta:
        indexes = [
            models.Index(fields=['rank', 'comment', 'writeup', 'author', 'created_at'])
        ]





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



