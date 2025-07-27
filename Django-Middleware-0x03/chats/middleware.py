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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limit = 5  # Max messages per minute
        self.time_window = 60  # Time window in seconds (1 minute)

    def __call__(self, request):
        # Get client IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Only process POST requests (assumed to be chat messages)
        if request.method == 'POST':
            current_time = time_module.time()

            # Clean up old timestamps outside the time window
            message_counts[ip_address] = [
                (ts, count) for ts, count in message_counts[ip_address]
                if current_time - ts <= self.time_window
            ]

            # Count total messages in the current time window
            total_messages = sum(count for _, count in message_counts[ip_address])

            # Check if the limit is exceeded
            if total_messages >= self.message_limit:
                return HttpResponse(
                    "Rate limit exceeded: Only 5 messages per minute allowed.",
                    status=429
                )

            # Increment message count for this IP
            message_counts[ip_address].append((current_time, 1))

        # Proceed with the request
        response = self.get_response(request)
        return response

# Existing RestrictAccessByTimeMiddleware (included for completeness)
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response