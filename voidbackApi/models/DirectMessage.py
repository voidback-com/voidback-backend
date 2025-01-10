from django.db import models
from .Account import Account
from .Post import Post
import hashlib, os


class DMImage(models.Model):
    image = models.ImageField(upload_to=f"images/dm/{hashlib.sha256(os.urandom(16)).hexdigest()}/", blank=False, null=False)

    def __str__(self):
        return str(self.pk)


class DMVoiceNote(models.Model):
    voiceNote = models.FileField(upload_to=f"voiceNotes/dm/{hashlib.sha256(os.urandom(16)).hexdigest()}/", blank=False, null=False)

    def __str__(self):
        return str(self.pk)



class DirectMessageSession(models.Model):
    # for a session to be established the session initiator must be followed by the reciepient
    initiator = models.ForeignKey(Account, related_name="initiator", on_delete=models.CASCADE)
    friend = models.ForeignKey(Account, related_name="friend", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["initiator", 'friend', 'created_at'])
        ]




class DMMessage(models.Model):
    session = models.ForeignKey(DirectMessageSession, on_delete=models.CASCADE, related_name="session")
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sender")
    message = models.TextField(max_length=5000, blank=False)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True) # attached post
    image = models.ForeignKey(DMImage, on_delete=models.CASCADE, blank=True, null=True) # attached image
    voiceNote = models.ForeignKey(DMVoiceNote, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey("InboxMessage", on_delete=models.DO_NOTHING, null=True, blank=True) # reply message
    sent_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False, blank=True)
    seen_at = models.DateTimeField(auto_now=True)


    class Meta:
        indexes = [
            models.Index(fields=["session", 'sender', "seen", "seen_at", "sent_at"])
        ]


    def __str__(self):
        return str(self.pk)





