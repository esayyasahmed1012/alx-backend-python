from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Create a notification for the receiver when a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Log the old content of a message before it is updated.
    """
    if instance.id:  # Check if the instance already exists (i.e., it's an update)
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:  # Only log if content has changed
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True  # Mark message as edited
        except Message.DoesNotExist:
            pass  