from rest_framework import serializers
from apps.custom_user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False}
        }

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data and validated_data['username'] == instance.username:
            validated_data.pop('username')
        if 'password' in validated_data and validated_data['password'] == instance.password:
            validated_data.pop('password')
        return super().update(instance, validated_data)


class CustomUserLoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации."""
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(required=True, write_only=True)