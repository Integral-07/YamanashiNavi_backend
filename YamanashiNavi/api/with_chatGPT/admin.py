from django.contrib import admin
from .models import Message
from .models import CustomUser

admin.site.register(Message)
admin.site.register(CustomUser)
