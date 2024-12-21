from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Message(models.Model):
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_owner")