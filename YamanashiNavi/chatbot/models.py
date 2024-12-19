from django.db import models

class Message(models.Model):

    system_prompt = models.TextField(verbose_name="システムプロンプト", blank=True, null=True)
    prompt = models.TextField(verbose_name="プロンプト", blank=True, null=True)
