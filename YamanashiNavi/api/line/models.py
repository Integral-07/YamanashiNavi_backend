from django.db import models

class Session(models.Model):

    user_id = models.CharField('line識別子', max_length=200, primary_key=True)
    conversation_id = models.CharField('会話id', max_length=200)
    lang_setting = models.CharField('言語設定', max_length=10)

    def __str__(self):

        return f"{self.user_id} <convID: {self.conversation_id}[ {self.lang_setting} ]>"
