from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show conversations where the authenticated user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # Create a new conversation with participants
        participant_ids = request.data.get('participant_ids', [])
        if not participant_ids:
            return Response({"error": "At least one participant ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the authenticated user is included
        if str(request.user.user_id) not in participant_ids:
            participant_ids.append(str(request.user.user_id))

        # Validate participant IDs
        try:
            participants = User.objects.filter(user_id__in=participant_ids)
            if len(participants) < 2:
                return Response({"error": "A conversation must have at least two participants."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid participant ID(s)."}, status=status.HTTP_400_BAD_REQUEST)

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show messages in conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # Create a new message in an existing conversation
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "conversation_id and message_body are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            if not conversation.participants.filter(user_id=request.user.user_id).exists():
                return Response({"error": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        except Conversation.DoesNotExist:
            return Response({"error": "Invalid conversation ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Create message
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)