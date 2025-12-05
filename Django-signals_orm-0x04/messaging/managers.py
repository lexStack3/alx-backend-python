from django.db import models


class UnreadMessagesManager(models.Manager):
    """Custome ORM Manager for Unread Messages."""
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only(
            "message_id", "sender", "receiver", "content", "timestamp"
        )
