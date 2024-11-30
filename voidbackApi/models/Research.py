from datetime import timezone
from django.db import models
from .Account import Account
from django_resized import ResizedImageField



class ResearchPaper(models.Model):
    title = models.TextField(max_length=80, unique=True)
    # thumbnail = models.ImageField(upload_to="images/", blank=False, null=False)
    thumbnail = ResizedImageField(size=[1280, 720], upload_to="images/", blank=False, quality=100, keep_meta=False)
    pdf = models.FileField(upload_to="pdfs/", blank=False, null=False)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'author', 'created_at'])
        ]


    def __str__(self):
        return self.title







class ResearchPaperImpression(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, to_field="id", related_name="paperImpression")
    impression = models.IntegerField(default=0, blank=True, editable=True) # (0 = view), (1 = viewed and liked) and (-1 = viewed and disliked)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    hash = models.TextField(blank=True, unique=True) # username:post_id
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['paper', 'account', 'impression', 'created_at', "updated_at"])
        ]


    def __str__(self):
        return self.paper.title




