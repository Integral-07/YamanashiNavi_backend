from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser

import uuid

class Message(models.Model):
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_owner")

class CustomUser(AbstractUser):

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.username