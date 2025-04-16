from rest_framework import serializers
from apps.custom_user.models import CustomUser
from apps.med_personal.models import Doctor, Registrar
from apps.custom_user.serializers import CustomUserSerializer


class ShortDoctorSerializer(serializers.ModelSerializer):
    """Сериализатор для короткой информации о докторе."""
    url = serializers.HyperlinkedIdentityField(
        view_name='doctor-detail',
        lookup_field='id'
    )

    class Meta:
        model = Doctor
        fields = [
            'id',
            'url',
            'full_name',
            'specialties'
        ]


class FullDoctorSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о докторе."""
    url = serializers.HyperlinkedIdentityField(
        view_name='doctor-detail',
        lookup_field='id'
    )
    user = CustomUserSerializer()
    hospital_url = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id',
            'url',
            'user',
            'middle_name',
            'phone_number',
            'specialization',
            'hospital',
            'hospital_url',
        ]

    def get_hospital_url(self, obj):
        if obj.hospital:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/medical_hub/hospitals/{obj.hospital.id}/')
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'doctor'
        user = CustomUser.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if (user_data and
                any(k not in ['username', 'password'] or v != getattr(instance.user, k) for k, v in user_data.items())):
            user_serializer = CustomUserSerializer(instance=instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RegistrarSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о регистратуре."""
    url = serializers.HyperlinkedIdentityField(
        view_name='registrar-detail',
        lookup_field='id'
    )
    user = CustomUserSerializer()
    hospital_url = serializers.SerializerMethodField()

    class Meta:
        model = Registrar
        fields = [
            'id',
            'url',
            'user',
            'middle_name',
            'phone_number',
            'hospital',
            'hospital_url'
        ]

    def get_hospital_url(self, obj):
        if obj.hospital:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/medical_hub/hospitals/{obj.hospital.id}/')
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'registrar'
        user = CustomUser.objects.create_user(**user_data)
        registrar = Registrar.objects.create(user=user, **validated_data)
        return registrar

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if (user_data and
                any(k not in ['username', 'password'] or v != getattr(instance.user, k) for k, v in user_data.items())):
            user_serializer = CustomUserSerializer(instance=instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance