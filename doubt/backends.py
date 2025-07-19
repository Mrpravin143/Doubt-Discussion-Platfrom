from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email__iexact=username)  # case-insensitive
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None
