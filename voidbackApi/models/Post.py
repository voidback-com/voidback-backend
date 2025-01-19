from datetime import timezone
from django.db import models
from .Account import Account


class PostImage(models.Model):
    image = models.ImageField(upload_to="images/", blank=False, null=False)

    def __str__(self):
        return str(self.pk)



class Hashtag(models.Model):
    hashtag = models.TextField(max_length=30, blank=False, null=False, unique=True)
    rank = models.BigIntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.hashtag


    class Meta:
        indexes = [
            models.Index(fields=['hashtag', "rank", 'created_at',  "updated_at"])
        ]





class Symbol(models.Model):
    symbol = models.TextField(max_length=15, blank=False, null=False, unique=True)
    rank = models.BigIntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

    class Meta:
        indexes = [
            models.Index(fields=['symbol', "rank", 'created_at', "updated_at"])
        ]





class Post(models.Model):
    content = models.JSONField()

    image = models.ForeignKey(PostImage, related_name="post_image", blank=True, on_delete=models.CASCADE, null=True)
    video = models.TextField(null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="post_hashtags", blank=True)
    symbols = models.ManyToManyField(Symbol, related_name="post_symbols", blank=True)
    mentions = models.ManyToManyField(Account, related_name="post_mentions", blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True, to_field="id")
    from_mobile = models.BooleanField(default=False, blank=True, null=True) # rendered differently on the browser when from the mobile editor
    rank = models.BigIntegerField(default=0, blank=True, null=True)


    def __str__(self):
        return str(self.pk)


    class Meta:
        indexes = [
            models.Index(fields=["author", "parent_post", "rank", 'created_at', "updated_at"])
        ]




class PostImpression(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field="id", related_name="post_impression")
    impression = models.IntegerField(default=0, blank=True, editable=True) # (0 = view), (1 = viewed and liked) and (-1 = viewed and disliked)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    hash = models.TextField(blank=True, unique=True) # username:post_id
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.pk)


    class Meta:
        indexes = [
            models.Index(fields=['post', 'account', 'impression', 'created_at', "updated_at"])
        ]







class PostMetadata(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field="id")
    symbols = models.JSONField()
    hashtags = models.JSONField()
    text_sentiment = models.TextField()
    partial_sentiment = models.JSONField(null=True)
    text_toxicity = models.JSONField()
    text = models.TextField(max_length=20000) # post text limit is 20k chars


    def __str__(self):
        return str(self.post.pk)


    class Meta:
        indexes = [
            models.Index(fields=['post', 'symbols', 'hashtags', 'text_sentiment', 'partial_sentiment', 'text_toxicity', 'text'])
        ]




class ForYou(models.Model):
    symbols = models.JSONField()
    hashtags = models.JSONField()
    accounts = models.JSONField()
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        indexes = [
            models.Index(fields=['account', 'symbols', 'hashtags', 'accounts', 'created_at', "updated_at"])
        ]


    def __str__(self):
        return self.account.username



 

