from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser

class users(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('first_name'),max_length=255)
    last_name = models.CharField(_('last_name'),max_length=255)
    password = models.CharField(_('password'), max_length=128)
    birthdate = models.DateField(blank=True, null=True)
    last_seen = models.DateTimeField(default=timezone.now())

    

    def __str__(self):
        return self.username

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(users, related_name='conversation')
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(users, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now())
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} in Conversation {self.conversation.conversation_id}"