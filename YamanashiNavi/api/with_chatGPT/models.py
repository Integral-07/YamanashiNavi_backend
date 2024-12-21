from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

class Message(models.Model):
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

"""
class User(AbstractUser):

    user_identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.user_identifier})"

"""