from django.db import models

class Message(models.Model):
    role = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=10000)
    convasation_id = models.CharField(max_length=1000, default="")
    #models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_owner")