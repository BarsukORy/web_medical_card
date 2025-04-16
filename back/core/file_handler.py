import logging
import os
import shutil
from django.core.files.storage import default_storage
from back import settings

logger = logging.getLogger(__name__)


class FileHandler:
    """Класс для обработки файлов."""
    @staticmethod
    def save_file(instance, file_field_name: str, path_function) -> str:
        file_field = getattr(instance, file_field_name)
        if file_field:
            try:
                original_filename = os.path.basename(file_field.name)
                name, ext = os.path.splitext(original_filename)
                if len(name) > 100:
                    name = name[:100]
                    original_filename = f'{name}{ext}'
                new_name = path_function(instance, original_filename)
                saved_path = default_storage.save(new_name, file_field)
                setattr(instance, file_field_name, saved_path)
                return saved_path
            except Exception as e:
                logger.error(f"Ошибка при сохранении файла {file_field.name}: {e}")
                return ''

    @staticmethod
    def delete_file(file_path: str) -> None:
        if file_path and default_storage.exists(file_path):
            try:
                default_storage.delete(file_path)
            except Exception as e:
                logger.error(f"Ошибка при удалении файла {file_path}: {e}")

    @staticmethod
    def delete_patient_folder(instance) -> None:
        from apps.patient.utils import generate_name_folder_for_patient
        folder_path = generate_name_folder_for_patient(instance)
        folder_path = os.path.join(settings.MEDIA_ROOT, f'patients/{folder_path}')
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                logger.error(f"Ошибка при удалении папки {folder_path}: {e}")

    @staticmethod
    def delete_folder_if_empty(folder_path: str) -> None:
        if os.path.exists(folder_path):
            dir_contents = os.listdir(folder_path)
            if not dir_contents:
                try:
                    os.rmdir(folder_path)
                    logger.info(f"Удалена пустая папка: {folder_path}")
                except Exception as e:
                    logger.error(f"Ошибка при удалении папки {folder_path}: {e}")
            else:
                logger.info(f"Папка {folder_path} не пуста, содержимое: {dir_contents}")
        else:
            logger.warning(f"Папка не существует: {folder_path}")

    @staticmethod
    def delete_file_and_delete_directory_is_empty(file_path: str) -> None:
        if file_path:
            FileHandler.delete_file(file_path)
            folder_path = os.path.dirname(file_path)
            absolute_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            FileHandler.delete_folder_if_empty(absolute_folder_path)