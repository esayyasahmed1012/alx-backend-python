from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

@login_required
def inbox(request):
    """
    Display unread messages for the current user.
    """
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages
    })

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user not in [message.sender, message.receiver]:
        return render(request, 'messaging/error.html', {'error': 'Unauthorized access'})
    
    history = message.history.all()
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.sender:
        return render(request, 'messaging/error.html', {'error': 'Only the sender can edit this message'})
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message.content = content
            message.edited_by = request.user
            message.save()
            messages.success(request, 'Message updated successfully')
            return redirect('message_history', message_id=message.id)
        else:
            messages.error(request, 'Content cannot be empty')
    
    return render(request, 'messaging/edit_message.html', {'message': message})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('login')
    return render(request, 'messaging/delete_user.html', {})

@login_required
def threaded_conversation(request, message_id):
    """
    Display a threaded conversation starting from the root message.
    """
    messages = Message.objects.filter(
        Q(id=message_id) & (Q(sender=request.user) | Q(receiver=request.user))
    ).select_related('sender', 'receiver', 'parent_message').prefetch_related('replies').only(
        'id', 'sender__username', 'receiver__username', 'content', 'timestamp',
        'edited', 'edited_by__username', 'parent_message__id', 'read'
    )
    
    if not messages.exists():
        return render(request, 'messaging/error.html', {'error': 'Message not found or unauthorized access'})
    
    root_message = messages.first()
    # Mark the root message as read if the user is the receiver
    if request.user == root_message.receiver and not root_message.read:
        root_message.read = True
        root_message.save()
    
    return render(request, 'messaging/threaded_conversation.html', {
        'root_message': root_message
    })

@login_required
def reply_message(request, message_id):
    parent_message = get_object_or_404(Message, id=message_id)
    if request.user not in [parent_message.sender, parent_message.receiver]:
        return render(request, 'messaging/error.html', {'error': 'Unauthorized access'})
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            receiver = parent_message.sender if request.user == parent_message.receiver else parent_message.receiver
            if request.user == parent_message.receiver and not parent_message.read:
                parent_message.read = True
                parent_message.save()
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                parent_message=parent_message
            )
            messages.success(request, 'Reply sent successfully')
            return redirect('threaded_conversation', message_id=message_id)
        else:
            messages.error(request, 'Content cannot be empty')
    
    return render(request, 'messaging/reply_message.html', {'parent_message': parent_message})