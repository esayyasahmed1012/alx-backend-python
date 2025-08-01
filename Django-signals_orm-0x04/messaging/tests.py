from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification
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