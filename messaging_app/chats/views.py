from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, users
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    UserRegisterSerializer
)
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import AllowAny


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['sent_at']  
    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('conversation', 'sender').order_by('sent_at')

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = users.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
