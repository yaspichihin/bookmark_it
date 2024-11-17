from django.contrib.auth.models import User

from .models import Profile


class EmailAuthBackend:
    """
    Аутентификация посредством адреса электронной почты.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """
    Создание профиля пользователя для социальной аутентификации.
    """
    Profile.objects.get_or_create(user=user)
