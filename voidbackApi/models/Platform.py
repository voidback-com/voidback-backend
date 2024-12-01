from django.db import models
from .Account import Account




class PlatformMessage(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    # links example: [{"label": "contact us", "link": "/contact/us", "isInternal": true}]
    links = models.JSONField(blank=True, null=True) 

    # links = array(object(label: str, link: str, isInternal: bool))


    author = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["title", 'author', 'created_at', 'description'])
        ]

  
    def __str__(self):
        return self.title




class PlatformMessageImpression(models.Model):
    message = models.ForeignKey(PlatformMessage, on_delete=models.DO_NOTHING, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["message", "account", "created_at"])
        ]


    def __str__(self):
        return str(self.pk)






