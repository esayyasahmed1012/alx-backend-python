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

from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from datetime import time, timedelta
from collections import defaultdict
import time as time_module

# In-memory store for message counts (IP -> [(timestamp, count)])
message_counts = defaultdict(list)

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Access denied: Authentication required.")

        # Check if user has admin or moderator role
        try:
            user_role = request.user.role.lower()  # Assuming role is a field on the user model
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: Only admins or moderators allowed.")
        except AttributeError:
            return HttpResponseForbidden("Access denied: User role not defined.")

        # Proceed with the request if user has required role
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = timezone.now().time()
        start_time = time(21, 0)  # 9PM
        end_time = time(18, 0)    # 6PM
        if not (start_time <= current_time or current_time <= end_time):
            return HttpResponseForbidden("Access to messaging is restricted between 6PM and 9PM.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limit = 5  # Max messages per minute
        self.time_window = 60  # Time window in seconds (1 minute)

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if request.method == 'POST':
            current_time = time_module.time()
            message_counts[ip_address] = [
                (ts, count) for ts, count in message_counts[ip_address]
                if current_time - ts <= self.time_window
            ]
            total_messages = sum(count for _, count in message_counts[ip_address])
            if total_messages >= self.message_limit:
                return HttpResponse(
                    "Rate limit exceeded: Only 5 messages per minute allowed.",
                    status=429
                )
            message_counts[ip_address].append((current_time, 1))
        response = self.get_response(request)
        return response