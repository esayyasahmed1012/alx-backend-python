from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.utils import timezone

class MessageNotificationTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(
            username='sender', password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver', password='testpass123'
        )

    def test_message_creation_triggers_notification(self):
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )

        # Check if notification was created
        notification = Notification.objects.filter(
            user=self.receiver,
            message=message
        ).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
        self.assertTrue(
            abs(notification.created_at - timezone.now()).total_seconds() < 60
        )

    def test_no_notification_for_existing_message(self):
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )

        # Update the message
        message.content = "Updated message"
        message.save()

        # Check notification count (should still be 1 from creation)
        notification_count = Notification.objects.filter(
            user=self.receiver,
            message=message
        ).count()
        self.assertEqual(notification_count, 1)

    def test_message_edit_creates_history(self):
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message"
        )

        # Update the message
        original_content = message.content
        message.content = "Edited message"
        message.save()

        # Check if history was created
        history = MessageHistory.objects.filter(message=message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, original_content)
        self.assertEqual(history.message, message)
        self.assertTrue(message.edited)
        self.assertTrue(
            abs(history.edited_at - timezone.now()).total_seconds() < 60
        )

    def test_no_history_for_unchanged_content(self):
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message"
        )

        # Update without changing content
        message.save()

        # Check no history was created
        history_count = MessageHistory.objects.filter(message=message).count()
        self.assertEqual(history_count, 0)
        self.assertFalse(message.edited)