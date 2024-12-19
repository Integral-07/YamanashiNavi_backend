from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source="pk") 

    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'timestamp']