from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Message


User = get_user_model()


def build_thread(message):
    """
    Recursively build nested thread of replies.
    """
    return {
        "message_id": str(message.message_id),
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "parent": str(message.parent_message.message_id) \
                if message.parent_message else None,
        "replies": [
            build_thread(reply) for reply in message.replies.all()
        ]
    }


@csrf_exempt
def delete_user(request, user_id):
    """
    Deletes a user account.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user.delete()

    return JsonResponse(
        {"message": "User and all related data deleted successfully"}
    )


@csrf_exempt
def list_users(request):
    """
    Lists all users.
    """
    users = User.objects.all().values(
        "user_id", "username",
        "email", "first_name",
        "last_name"
    )
    return JsonResponse({"users": list(users)}, status=200)


@login_required
@require_http_method(['GET', 'POST'])
def thread_view(request, user_id):
    """
    GET: Return the threaded conversation between current user and another user.
    POST: Creates a new message (optionally as a reply to an existing message)
    """
    receiver = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent_message = None

        if parent_id:
            parent_message = get_object_or_404(Message, message_id=parent_id)

        new_message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )

        return JsonResponse({
            "message": "Message created successfully",
            "message_id": str(new_message.message_id)
        })

    # GET: Fetch threaded conversation
    current_user = request.user
    qs Message.objects.filter(
        models.Q(sender=current_user, receiver=receiver)
        | models.Q(sender=receiver, receiver=current_user)
    ).select_related("sender", "receiver", "parent_message").prefetch_selected("replies").order_by("timestamp")

    # Only root messages (top-level)
    root_messages = qs.filter(parent_message__isnull=True)

    conversation_type = [build_thread(msg) for msg in root_messages]

    return JsonResponse({
        "conversation_between": f"{current_user.username} <-> {receiver.username}",
        "threaded_message": conversation_tree
    }, safe=False)
