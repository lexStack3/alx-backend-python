from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def notifyReceiver(sender, instance, created, **kwargs):
    if created:
        notfi = Notification.objects.create(
            sender=instance.sender,
            message=instance
        )


