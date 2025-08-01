from django.contrib import admin
from .models import Message, Notification, MessageHistory

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ['old_content', 'edited_at']
    can_delete = False

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'timestamp', 'edited']
    list_filter = ['timestamp', 'edited']
    search_fields = ['sender__username', 'receiver__username', 'content']
    date_hierarchy = 'timestamp'
    inlines = [MessageHistoryInline]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ['message', 'old_content', 'edited_at']
    list_filter = ['edited_at']
    search_fields = ['message__id', 'old_content']
    date_hierarchy = 'edited_at'