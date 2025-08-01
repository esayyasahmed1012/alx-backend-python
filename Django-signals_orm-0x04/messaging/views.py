from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Message

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
    message = get_object_or_404(Message.objects.prefetch_related('replies'), id=message_id)
    if request.user not in [message.sender, message.receiver]:
        return render(request, 'messaging/error.html', {'error': 'Unauthorized access'})
    
    return render(request, 'messaging/threaded_conversation.html', {
        'root_message': message
    })

@login_required
def reply_message(request, message_id):
    parent_message = get_object_or_404(Message, id=message_id)
    if request.user not in [parent_message.sender, parent_message.receiver]:
        return render(request, 'messaging/error.html', {'error': 'Unauthorized access'})
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Determine receiver: reply to the other user in the conversation
            receiver = parent_message.sender if request.user == parent_message.receiver else parent_message.receiver
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