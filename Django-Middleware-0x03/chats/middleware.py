from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Access denied: Authentication required.")

        try:
            user_role = request.user.role.lower()  # Assumes 'role' exists on User model
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: Only admins or moderators allowed.")
        except AttributeError:
            return HttpResponseForbidden("Access denied: User role not defined.")

        return self.get_response(request)
