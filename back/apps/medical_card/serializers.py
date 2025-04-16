from rest_framework import serializers
from apps.med_personal.models import Doctor
from apps.medical_card.models import (
    MedicalCard, MedicalCardEntry, MedicalCardEntryFile, Prescription, PrescriptionMedication
)
from apps.medical_hub.models import Hospital
from apps.patient.models import Patient
from apps.patient.serializers import ShortPatientSerializer
from apps.medical_hub.serializers import ShortHospitalSerializer
from apps.med_personal.serializers import ShortDoctorSerializer
from apps.catalog_medical_data.models import Disease, Medication
from core.pagination import MedicalCardEntryPagination


class ShortMedicalCardSerializer(serializers.ModelSerializer):
    """Сериализатор для краткой информации о мед карте."""
    url = serializers.HyperlinkedIdentityField(
        view_name='medical-card-detail',
        lookup_field='id'
    )
    short_info_patient = ShortPatientSerializer(read_only=True, source='patient')

    class Meta:
        model = MedicalCard
        fields = [
            'id',
            'url',
            'short_info_patient',
            'blood_type'
        ]


class ShortMedicalCardEntrySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    doctor_full_name = serializers.CharField(source='doctor.full_name', read_only=True, allow_null=True)

    class Meta:
        model = MedicalCardEntry
        fields = [
            'id',
            'url',
            'get_diagnosis',
            'doctor_full_name',
            'visit_date',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        medical_card_id = self.context.get('view').kwargs.get('medical_card_id')
        if not medical_card_id and hasattr(obj, 'medical_card'):
            medical_card_id = obj.medical_card.id
        if request and medical_card_id:
            return request.build_absolute_uri(f'/medical_card/medical-cards/{medical_card_id}/entries/{obj.id}/')
        return None

    # def get_doctor_full_name(self, obj):
    #     return obj.doctor.full_name if obj.doctor else None


class FullMedicalCardSerializer(serializers.ModelSerializer):
    """Сериализатор для полной информации о мед карте."""
    url = serializers.HyperlinkedIdentityField(
        view_name='medical-card-detail',
        lookup_field='id'
    )
    short_info_patient = ShortPatientSerializer(read_only=True, source='patient')
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source='patient',
        write_only=True,
        required=False
    )
    attachment_hospital_info = ShortHospitalSerializer(
        source='attachment_hospital',
        read_only=True
    )
    attachment_hospital_id = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.all(),
        source='attachment_hospital',
        write_only=True,
        required=False
    )
    entries = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCard
        fields = [
            'id',
            'url',
            'short_info_patient',
            'patient_id',
            'attachment_hospital_id',
            'attachment_hospital_info',
            'blood_type',
            'allergies',
            'chronic_diseases',
            'entries'
        ]
        read_only_fields = ['patient_id']

    def get_entries(self, obj):
        request = self.context.get('request')
        queryset = MedicalCardEntry.objects.filter(medical_card=obj)

        visit_date = request.query_params.get('visit_date')
        diagnosis_id = request.query_params.get('diagnosis')

        if visit_date:
            queryset = queryset.filter(visit_date=visit_date)
        if diagnosis_id:
            queryset = queryset.filter(diagnosis_id=diagnosis_id)

        paginator = MedicalCardEntryPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ShortMedicalCardEntrySerializer(page, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data

    def validate(self, data):
        if self.context['request'].method in ['POST']:
            patient = data.get('patient')
            if not patient:
                raise serializers.ValidationError({'patient': 'Пациент обязателен'})
            if MedicalCard.objects.filter(patient=patient).exists():
                raise serializers.ValidationError({'patient': 'Пациент уже имеет медицинскую карту'})
        return data


class MedicalCardEntryFileSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о файлах для записей в мед карте."""
    url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MedicalCardEntryFile
        fields = [
            'id',
            'url',
            'file_name',
            'file'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        medical_card_entry_id = obj.medical_card_entry_id
        if request and medical_card_entry_id:
            return request.build_absolute_uri(
                f'/medical_card/medical-card-entries/{medical_card_entry_id}/files/{obj.id}/')
        return None

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1] if obj.file else None

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('Вес файла не должен превышать 5 МБ')
        return value

    def create(self, validated_data):
        medical_card_entry_id = self.context['view'].kwargs.get('medical_card_entry_id')
        medical_card_entry = MedicalCardEntry.objects.get(id=medical_card_entry_id)
        validated_data['medical_card_entry'] = medical_card_entry
        return super().create(validated_data)


class MedicalCardEntrySerializer(serializers.ModelSerializer):
    """Сериализатор для информации о записях в мед карте."""
    url = serializers.SerializerMethodField()
    doctor = ShortDoctorSerializer(read_only=True)
    hospital_info = ShortHospitalSerializer(
        source='hospital',
        read_only=True
    )
    hospital_id = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.all(),
        source='hospital',
        write_only=True,
        required=False
    )
    diagnosis = serializers.PrimaryKeyRelatedField(
        queryset=Disease.objects.all(),
        required=False
    )
    files = MedicalCardEntryFileSerializer(
        many=True,
        read_only=True
    )
    disease_url = serializers.SerializerMethodField()
    prescription_url = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCardEntry
        fields = [
            'id',
            'url',
            'doctor',
            'visit_date',
            'hospital_id',
            'hospital_info',
            'diagnosis',
            'disease_url',
            'custom_diagnosis',
            'treatment',
            'custom_treatment',
            'notes',
            'files',
            'prescription_url'
        ]
        read_only_fields = [
            'doctor',
            'hospital_info',
            'files'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        medical_card_id = self.context.get('view').kwargs.get('medical_card_id')
        if request and medical_card_id:
            return request.build_absolute_uri(f'/medical_card/medical-cards/{medical_card_id}/entries/{obj.id}/')
        return None

    def get_disease_url(self, obj):
        if obj.diagnosis:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/catalog/diseases/{obj.diagnosis.id}/')

    def get_prescription_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/medical_card/medical-card-entries/{obj.id}/prescriptions/')
        return None

    def validate(self, data):
        diagnosis = data.get('diagnosis')
        custom_diagnosis = data.get('custom_diagnosis', '')
        if diagnosis and custom_diagnosis:
            raise serializers.ValidationError({'diagnosis': 'Выберите только один тип диагноза'})
        if not diagnosis and not custom_diagnosis:
            raise serializers.ValidationError({'diagnosis': 'Укажите диагноз или пользовательский диагноз'})
        if self.context['request'].method in ['POST']:
            visit_date = data.get('visit_date')
            if not visit_date:
                raise serializers.ValidationError({'visit_date': 'Дата визита обязательна'})
        return data

    def create(self, validated_data):
        request = self.context['request']
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError({'doctor': 'Авторизованный пользователь не является врачом'})
        medical_card_id = self.context['view'].kwargs.get('medical_card_id')
        try:
            medical_card = MedicalCard.objects.get(id=medical_card_id)
        except MedicalCard.DoesNotExist:
            raise serializers.ValidationError({'medical_card': 'Медицинская карта не найдена'})
        validated_data['doctor'] = doctor
        validated_data['medical_card'] = medical_card
        if 'diagnosis' not in validated_data:
            validated_data['diagnosis'] = None
        instance = MedicalCardEntry(**validated_data)
        if instance.check_duplicate(doctor, instance.visit_date, instance.diagnosis, instance.custom_diagnosis):
            raise serializers.ValidationError({'non_field_error': 'Запись с такими данными уже существует'})
        instance.save()
        return instance


class PrescriptionMedicationSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о назначениях на прием препаратов."""
    url = serializers.SerializerMethodField()
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())

    class Meta:
        model = PrescriptionMedication
        fields = [
            'id',
            'url',
            'medication',
            'dosage',
            'frequency',
            'duration',
            'individual_notes'
        ]
        read_only_fields = ['prescription']

    def get_url(self, obj):
        request = self.context.get('request')
        prescription_id = self.context.get('view').kwargs.get('prescription_id')
        if request and prescription_id:
            return request.build_absolute_uri(
                f'/medical_card/prescriptions/{prescription_id}/medications/{obj.id}/')
        return None

    def validate(self, data):
        prescription_id = self.context['view'].kwargs.get('prescription_id')
        prescription = Prescription.objects.get(id=prescription_id)
        medication = data.get('medication')
        if PrescriptionMedication.objects.filter(prescription=prescription, medication=medication).exists():
            raise serializers.ValidationError({'medication': 'Данный препарат уже был назначен'})
        return data

    def create(self, validated_data):
        prescription_id = self.context['view'].kwargs.get('prescription_id')
        prescription = Prescription.objects.get(id=prescription_id)
        validated_data['prescription'] = prescription
        return super().create(validated_data)


class PrescriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о назначениях."""
    url = serializers.SerializerMethodField()
    medications = PrescriptionMedicationSerializer(read_only=True, many=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'url',
            'administration_notes',
            'medications'
        ]
        read_only_fields = [
            'medications'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        medical_card_entry_id = self.context.get('view').kwargs.get('medical_card_entry_id')
        if request and medical_card_entry_id:
            return request.build_absolute_uri(
                f'/medical_card/medical-card-entries/{medical_card_entry_id}/prescriptions/{obj.id}/')
        return None

    def create(self, validated_data):
        medical_card_entry_id = self.context['view'].kwargs.get('medical_card_entry_id')
        medical_card_entry = MedicalCardEntry.objects.get(id=medical_card_entry_id)
        validated_data['medical_card_entry'] = medical_card_entry
        return super().create(validated_data)
