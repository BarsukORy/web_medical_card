from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        """Функция для проверки прав на владельца записи или админа."""
        if request.user.is_superuser or request.user.is_staff:
            return True
        return obj.pk == request.user


class IsRegistrarOrAdmin(BasePermission):
    # def has_permission(self, request, view):
    #     """
    #     Функция для проверки прав:
    #     создавать записи могут все авторизованные, а обновлять и удалять только регистратура и админы.
    #     """
    #
    #     if view.action == 'create':
    #         return request.user.is_authenticated
    #     return (
    #             request.user.is_authenticated
    #             and (request.user.role == 'registrar' or request.user.is_staff or request.user.is_superuser)
    #     )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Функция для проверки прав:
        смотреть могут все авторизованные, а другие операции только админы и регистратура.
        """
        if request.method in ['GET']:
            return True
        return (
                request.user.is_superuser
                or request.user.is_staff
                or request.user.role == 'registrar'
        )

