from django.db import models
from django.contrib.auth.models import User

class HistoryModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    conversation_id = models.CharField(verbose_name='会話id', max_length=200, default="")

    class Meta:
        db_table = "history"
        verbose_name = "会話履歴"


    def __str__(self):
        return f"{self.user.username}"
        


class MessageModel(models.Model):

    ROLE_CHOICES = [
        ('user', 'ユーザ'),
        ('ai', 'AI')
    ]

    owner = models.ForeignKey(HistoryModel, on_delete=models.CASCADE, related_name="owner")
    role = models.CharField(default="user", max_length=10, verbose_name="役割", choices=ROLE_CHOICES)
    content = models.TextField(max_length=1000, verbose_name="内容")
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name="タイムスタンプ")

    def __str__(self):
        return f"{self.owner} : {self.role}> {self.content}({self.time_stamp})"