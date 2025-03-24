from rest_framework import serializers
from .models import HistoryModel, MessageModel

class MessageSerializer(serializers.ModelSerializer):

    class Meta:

        model = MessageModel
        fields = ['id', 'role', 'content', 'time_stamp']


class HistorySerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.CharField(source="user.id", read_only=True)
    messages = MessageSerializer(many=True, source="owner", read_only=True)

    class Meta:

        model = HistoryModel
        fields = ['user_id', 'user_name', 'messages']

        


