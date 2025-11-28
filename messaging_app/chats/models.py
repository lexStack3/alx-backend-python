import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ('guest', 'Guest'),
    ('host', 'Host'),
    ('admin', 'admin')
)

class User(AbstractUser):
    """A model representation of a <User> instance."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    password = models.CharField(max_length=128, blank=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES,
                            default='guest')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]

    def __str__(self):
        """String representation of a <User> instance."""
        return self.username


class Conversation(models.Model):
    """A model representation of a <Conversation> instance."""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                       editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a <Conversation> instance."""
        return f"conversation: {self.conversation_id}"


class Message(models.Model):
    """A model representation of a <Message> instance."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField(max_length=2048, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of a <Message> instance."""
        return self.message_body
