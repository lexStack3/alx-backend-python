from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Message, Conversation


class BlockAnonymous(permissions.BasePermission):
    """
    Blocks Anonymous accounts.
    """
    message = "Anonymous users are not allowed to perform this action."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied(self.message)
        return True


class IsMessageOwner(permissions.BasePermission):
    """
    Allow access to the owner of a message.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender


class IsParticipantOfConversation(permissions.BasePermission):
    """
    - Deny anonymous users
    - Allow only participants of a conversation to access or modify
      messages/conversations
    """
    message = "Anonymous users are not allowed to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied(self.message)
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if isinstance(obj, Conversation):
            conversation = obj
        elif isinstance(obj, Message):
            conversation = obj.conversation
        else:
            return False

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return user in conversation.participants.all()

        return user in conversation.participants.all()
