from .models import SocialUser
from django.contrib.auth.backends import ModelBackend


class PhoneNumberAuthBackend:
    """Authentication backend that allows users to log in with their phone number."""

    def authenticate(self, request, **kwargs):
        """Authenticates a user based on phone number and password."""
        try:
            user = SocialUser.objects.get(phone=kwargs.get('username'), is_deleted=False, is_active=True)
            if user.check_password(kwargs.get('password')):
                return user
            return None
        except (SocialUser.DoesNotExist, SocialUser.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """Retrieves a user by their primary key."""
        try:
            return SocialUser.objects.get(pk=user_id)
        except SocialUser.DoesNotExist:
            return None


class CustomModelBackend(ModelBackend):
    """Custom authentication backend that ensures users are active and not is_deleted."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticates a user based on username and password, ensuring they are active and not is_deleted."""
        try:
            user = SocialUser.objects.get(username=username)
            if user.check_password(password) and user.is_active and not user.is_deleted:
                return user
        except SocialUser.DoesNotExist:
            return None