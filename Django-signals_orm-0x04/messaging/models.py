import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Model representation of a User instance.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name"
    ]

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        """
        String representation of a <User> instance.
        """
        return self.username


class Message(models.Model):
    """
    Model representation of a Message instance.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def get_thread(self):
        """
        Returns a message and all its replies in a nested dict structure.
        This method uses recursion to build threaded conversation trees.
        """
        return {
            "message_id": str(self.message_id),
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "content": self.content,
            "created_at": self.created_at,
            "replies": [
                reply.get_thread() for reply in self.replies.all()
            ]
        }

    @staticmethod
    def fetch_conversation(sender, receiver):
        """
        Efficiently fetch all messages between two users using select_related
        and prefecth_related to minimize database queries.
        """
        return (
            Message.objects
            .filter(sender__in=[sender, receiver], receiver__in[sender, receiver])
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
            .order_by("timestamp")
        )


    def __str__(self):
        """
        String representation of a <Message> instance.
        """
        return "Message {}: {} to {}".format(
            self.message_id,
            self.sender.username,
            self.receiver.username
        )


class Notification(models.Model):
    """
    Model representation of a <Notification> instance.
    """
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of a <Notification> instance.
        """
        return "Notif from {}: {}".format(
            self.sender.username,
            self.message.content[:20]
        )


class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    message_id = models.CharField(max_length=36)
    edited_by = models.CharField(max_length=128)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        A string representation of a <MessageHistory> instance.
        """
        return "History for {} at {}".format(
            self.message_id,
            self.edited_at
        )
