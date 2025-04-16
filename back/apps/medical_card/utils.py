import os
from apps.patient.utils import generate_name_folder_for_patient


def medical_card_entry_file_path(instance, filename: str) -> str:
    """Генерирует путь для файла записи медицинской карты."""
    patient_folder = generate_name_folder_for_patient(instance.medical_card_entry.medical_card.patient)
    entry_id = instance.medical_card_entry.id
    return f'patients/{patient_folder}/medical_card_entries/entry_{entry_id}/{os.path.basename(filename)}'