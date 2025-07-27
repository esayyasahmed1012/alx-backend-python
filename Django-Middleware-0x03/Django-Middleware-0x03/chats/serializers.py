from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display', read_only=True)  # Display role choice label
    full_name = serializers.SerializerMethodField()  # Computed field for full name

    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()  # Short preview of message body

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'message_preview', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'message_preview']

    def get_message_preview(self, obj):
        return obj.message_body[:50] + "..." if len(obj.message_body) > 50 else obj.message_body

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()  # Count of participants

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_count', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at', 'participant_count']

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value