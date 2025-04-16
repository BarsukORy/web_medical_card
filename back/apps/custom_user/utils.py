from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions

User = get_user_model()


def get_user(username: str) -> 'User':
    """Функция для получения пользователя."""
    try:
        return User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None


def get_and_authenticate_user(username: str, password: str) -> 'User':
    """Функция для авторизации."""
    user = get_user(username)
    if user is None or not user.check_password(password):
        raise exceptions.ValidationError('Неправильный пароль. Попробуйте снова.')
    return user
