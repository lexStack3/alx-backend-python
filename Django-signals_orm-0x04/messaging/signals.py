from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def notifyReceiver(sender, instance, created, **kwargs):
    """
    Notifies a receiver of a message.
    """
    if created:
        notfi = Notification.objects.create(
            sender=instance.sender,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_old_message(sender, instance, **kwargs):
    """
    Logs old content of a message before updating.
    """
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message_id=instance.message_id,
            edited_by=instance.sender.user_id,
            old_content=old_message.content
        )
        instance.edited = True
