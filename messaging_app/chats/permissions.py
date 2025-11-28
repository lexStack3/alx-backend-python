from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Message, Conversation


class BlockAnonymous(BasePermission):
    """
    Blocks Anonymous accounts.
    """
    message = "Anonymous users are not allowed to perform this action."

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied(self.message)
        return True


class IsMessageOwner(BasePermission):
    """
    Allow access to the owner of a message.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender


class IsConversationParticipant(BasePermission):
    """
    Allow access only if the user is part of a particular conversation.
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Conversation):
            return request.user in obj.conversation.participants.all()
        if not isinstance(obj, Message):
            return request.user in obj.participants.all()
