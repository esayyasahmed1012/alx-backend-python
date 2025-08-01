from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    # Ensure user is either sender or receiver
    if request.user not in [message.sender, message.receiver]:
        return render(request, 'messaging/error.html', {'error': 'Unauthorized access'})
    
    history = message.history.all()
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })