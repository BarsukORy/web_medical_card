from rest_framework.permissions import BasePermission


class OnlyReadOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        """
        Функция для проверки прав:
        смотреть могут все авторизованные, а другие операции только админы.
        """
        if request.method in ['GET']:
            return True
        return request.user.is_superuser or request.user.is_staff