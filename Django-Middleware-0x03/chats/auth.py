from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions  # Import the exceptions module

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        return user, token