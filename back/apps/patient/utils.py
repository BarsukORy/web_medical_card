import os
from back import settings
from django.core.exceptions import ValidationError


def generate_name_folder_for_patient(instance):
    """Генерирует название папки для пациента."""
    return str(instance.uuid)


def patient_photo_path(instance, filename):
    """Генерирует путь для фото пациента."""
    return os.path.join(f'patients/{generate_name_folder_for_patient(instance)}/faces', os.path.basename(filename))


def prepare_photo_directory(instance) -> None:
    """Подготавливает директорию и обновляет путь к фото."""
    if instance.photo:
        folder_path = generate_name_folder_for_patient(instance)
        patient_dir = os.path.join(settings.MEDIA_ROOT, f'patients/{folder_path}/faces')
        os.makedirs(patient_dir, exist_ok=True)


def generate_face_vector(self) -> None:
    """Генерирует вектор лица из фотографии."""
    from core.face_utils import generate_face_vector_sync
    if self.photo and os.path.exists(self.photo.path):
        try:
            self.face_vector = generate_face_vector_sync(self.photo)
        except ValueError as e:
            self.face_vector = None
            raise ValidationError(f"Ошибка генерации вектора лица: {e}")
    else:
        raise ValidationError(f"Файл фотографии не найден: {self.photo.path if self.photo else 'Фото отсутствует'}")