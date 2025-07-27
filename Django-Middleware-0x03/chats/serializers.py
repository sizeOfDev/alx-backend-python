from rest_framework import serializers
from .models import users, Conversation, Message
from django.contrib.auth.password_validation import validate_password

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'birthdate']
        read_only_fields = ['user_id']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = users
        fields = ['user_id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['user_id']

    def create(self, validated_data):
        user = users(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value 

class MessageSerializer(serializers.ModelSerializer):
    sender = UsersSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'read']
        read_only_fields = ['message_id', 'sent_at', 'sender']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UsersSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'last_message']

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        if last:
            return MessageSerializer(last).data
        return None
    
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
    queryset=users.objects.all(),
    many=True,
    pk_field=serializers.UUIDField()
)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at']

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value

    def create(self, validated_data):
        conversation = Conversation.objects.create()
        conversation.participants.set(validated_data['participants'])
        return conversation