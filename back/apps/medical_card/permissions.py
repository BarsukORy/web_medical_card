from rest_framework import permissions
from apps.med_personal.models import Doctor
from apps.medical_card.models import MedicalCardEntry, MedicalCardEntryFile, Prescription, PrescriptionMedication


class IsOwnerDoctorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Функция для проверки прав, чтобы созданную запись мед карты мог изменять только ее создатель или админ."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True
        try:
            doctor = Doctor.objects.get(user=request.user)
            if isinstance(obj, MedicalCardEntry):
                entry = obj
            elif isinstance(obj, MedicalCardEntryFile):
                entry = obj.medical_card_entry
            elif isinstance(obj, Prescription):
                entry = obj.medical_card_entry
            elif isinstance(obj, PrescriptionMedication):
                entry = obj.prescription.medical_card_entry
            else:
                return False
            return entry.doctor == doctor
        except Doctor.DoesNotExist:
            return False