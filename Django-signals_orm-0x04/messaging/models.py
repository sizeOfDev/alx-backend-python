from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.CharField(max_length=250)
    receiver = models.CharField(max_length=250)
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=datetime.now())
    edited = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"Notification for {self.user} - Read: {self.read}"

class  MessageHistory(models.Model):

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=datetime.now())