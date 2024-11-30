from django.db import models
from .Account import Account
from .Post import Post



class InboxMessage(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="from_account", to_field="username")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="to_account", to_field="username")
    caption = models.JSONField()
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        indexes = [
            models.Index(fields=["from_account", 'to_account', 'post', 'created_at'])
        ]



    def __str__(self):
        return str(self.pk)




