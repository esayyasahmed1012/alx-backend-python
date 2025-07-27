# import logging
# from datetime import datetime

# class RequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # Configure logging
#         logging.basicConfig(
#             filename='requests.log',
#             level=logging.INFO,
#             format='%(message)s',
#         )

#     def __call__(self, request):
#         user = request.user if request.user.is_authenticated else 'Anonymous'
#         log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
#         logging.info(log_entry)
#         response = self.get_response(request)
#         return response


# Django-Middleware-0x03/chats/middleware.py
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import time

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current time in server's timezone
        current_time = timezone.now().time()
        
        # Define allowed time range (9PM to 6PM)
        start_time = time(21, 0)  # 9PM
        end_time = time(18, 0)    # 6PM
        
        # Check if current time is outside allowed hours
        if not (start_time <= current_time or current_time <= end_time):
            return HttpResponseForbidden("Access to messaging is restricted between 6PM and 9PM.")
        
        # If time is within allowed range, proceed with request
        response = self.get_response(request)
        return response