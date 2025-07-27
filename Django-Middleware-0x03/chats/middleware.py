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

from django.http import HttpResponseForbidden

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