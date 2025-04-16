from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from apps.custom_user.utils import get_and_authenticate_user
from apps.custom_user.serializers import CustomUserLoginSerializer
from apps.med_personal.serializers import FullDoctorSerializer, RegistrarSerializer


User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):  # Переключаемся на ViewSet
    """API для аутентификации и управления сессиями пользователей."""
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserLoginSerializer  # Указываем дефолтный сериализатор
    serializer_class_map = {  # Переименовываем словарь
        'login': CustomUserLoginSerializer,
    }

    def get_serializer_class(self):
        """Возвращает класс сериализатора в зависимости от действия."""
        return self.serializer_class_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        """Переопределяем get_queryset, чтобы избежать ошибки."""
        return None

    @action(methods=['POST'], detail=False)
    def login(self, request):
        """Функция для входа."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        data = self._serialize_user_data(user)
        data['auth_token'] = token.key
        return Response(data=data, status=status.HTTP_200_OK)

    @method_decorator(csrf_exempt, name='dispatch')
    @action(methods=['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Функция для выхода."""
        request.user.auth_token.delete()
        data = {'success': 'Вы вышли из системы'}
        return Response(data=data, status=status.HTTP_200_OK)

    def _serialize_user_data(self, user):
        """Вспомогательный метод для сериализации данных пользователя по роли."""
        from apps.med_personal.models import Doctor
        if user.role == 'doctor':
            try:
                doctor = Doctor.objects.get(user=user)
                return FullDoctorSerializer(doctor, context={'request': self.request}).data
            except Doctor.DoesNotExist:
                return {}
        elif user.role == 'registrar':
            try:
                registrar = user.registrar
                return RegistrarSerializer(registrar, context={'request': self.request}).data
            except AttributeError:
                return {}
        return {}