from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
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
    if instance.id:
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
                # edited_by is set in the view
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Clean up related data when a user is deleted.
    """
    # Messages where user is sender or receiver are deleted via CASCADE
    # Notifications are deleted via CASCADE
    # Explicitly delete MessageHistory for messages that might remain
    # (e.g., if CASCADE didn't cover all cases)
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()