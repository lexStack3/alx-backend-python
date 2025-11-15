from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework import permissions
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list conversations and create new conversations.
    Only shows conversations the authenticated user participates in.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backend = [DjangoFilterBackend]
    filterset_fields = ['paticipants']

    def get_queryset(self):
        """
        Only returns converations where the logged-in user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        Authomatically adds the authenticated user as a participant
        when creating a new conversation.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list messages and send new messages in a conversation.
    Users can only interact with conversations.
    """
    queryset = Message.objects.all().select_related('conversation', 'sender')
    serializer_class = MessageSerializer
    filter_backend = [DjangoFilterBackend]
    filterset_fields = ['sender', 'conversation']

    def get_queryset(self):
        """
        Only returns messages from conversations the user participates in.
        """
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('conversation', 'sender').order_by('sent_at')

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        
        if not conversation.participants.filter(
            user_id=self.request.user.user_id
        ).exists():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
