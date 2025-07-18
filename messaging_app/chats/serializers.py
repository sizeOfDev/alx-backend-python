from rest_framework import serializers
from .models import users, Conversation, Message
from django.contrib.auth.password_validation import validate_password

class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = users
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'birthdate', 'password']
        read_only_fields = ['user_id']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user 

class MessageSerializer(serializers.ModelSerializer):
    sender = UsersSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'read']
        read_only_fields = ['message_id', 'sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UsersSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']