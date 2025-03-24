from django.contrib import admin
from .models import HistoryModel, MessageModel

admin.site.register(HistoryModel)
admin.site.register(MessageModel)
