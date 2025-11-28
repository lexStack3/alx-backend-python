from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.exceptions import PermissionDenied
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .auth import CustomJWTAuthentication
from .pagination import MessagePagination
from .filters import MessageFilter
from .permissions import (
    BlockAnonymous,
    IsMessageOwner,
    IsParticipantOfConversation
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list conversations and create new conversations.
    Only shows conversations the authenticated user participates in.
    """
    #queryset = Conversation.objects.prefetch_related('participants')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    
    # For Conversation filter
    filter_backend = [DjangoFilterBackend]
    filterset_fields = ['participants']
    # conversation_id required for nested routing (checker requirement)


    def get_queryset(self):
        """
        Only returns converations where the logged-in user is a participant.
        """
        if self.request.user.is_anonymous:
            return Conversation.objects.none()
        return Conversation.objects.prefetch_related(
            'participants'
        ).filter(participants=self.request.user)

    def perform_create(self, serializer):
        """
        #Authomatically adds the authenticated user as a participant
        when creating a new conversation.
        """
        if not self.request.user.is_authenticated:
            return Respond(
                {'detail': 'Forbidden'},
                status=HTTP_403_FORBIDDEN
            )

        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(
        detail=True,
        serializer_class=MessageSerializer,
        url_path='messages'
    )
    def messages(self, request, pk=None):
        """
        Lists all messages in a particular conversation.
        """
        conversation = self.get_object()
        message_qs = conversation.messages.all().order_by('sent_at')
        
        filtered_qs = MessageFilter(request.GET, queryset=message_qs).qs

        paginator = MessagePagination()
        page = paginator.paginate_queryset(filtered_qs, request)
        serializer = MessageSerializer(page, many=True)
        return Response(serializer.data)

    @messages.mapping.post
    def post_message(self, request, pk=None):
        """
        CREATE a message under a particular conversation.
        """
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list messages and send new messages in a conversation.
    Users can only interact with conversations.
    """
    queryset = Message.objects.all().select_related('conversation', 'sender')
    serializer_class = MessageSerializer
    permission_classes = [BlockAnonymous, IsMessageOwner]
    pagination_class = MessagePagination
    filter_backend = [MessageFilter, DjangoFilterBackend]
    filterset_fields = ['sender', 'conversation']

    def get_queryset(self):
        """
        Only returns messages from conversations the user participates in.
        """
        if self.request.user.is_anonymous:
            return Message.objects.none()

        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('conversation', 'sender').order_by('sent_at')

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required to create a messgae.")

        conversation = serializer.validated_data['conversation']
        
        if not conversation.participants.filter(
            user_id=self.request.user.user_id
        ).exists():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
