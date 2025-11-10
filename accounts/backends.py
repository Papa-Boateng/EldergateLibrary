# /Users/keinagai/Desktop/mystudy/EldergateLibrary/accounts/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import EldergateLibraryUser

class MultiModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = EldergateLibraryUser.objects.get(username=username)
        except EldergateLibraryUser.DoesNotExist:
            # User not found in our custom model, so let other backends handle it.
            return None

        # If user is found, proceed with password check.
        # This handles hashed passwords for Reader/Librarian.
        if check_password(password, user.password):
            return user

        # WARNING: Insecure fallback for plain-text passwords for Administrator.
        if user.model_name == 'Administrator' and user.password == password:
            return user

        # If password check fails, return None.
        return None
                

    def get_user(self, user_id):
        try:
            user = EldergateLibraryUser.objects.get(pk=user_id)
            return user
        except EldergateLibraryUser.DoesNotExist:
            return None