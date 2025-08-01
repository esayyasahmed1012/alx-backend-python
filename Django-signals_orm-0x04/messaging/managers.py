from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Filter unread messages where the user is the receiver.
        """
        return self.filter(receiver=user, read=False).only('id', 'sender__username', 'content', 'timestamp')