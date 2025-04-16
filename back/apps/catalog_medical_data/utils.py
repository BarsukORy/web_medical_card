from apps.catalog_medical_data.catalog import diseases, medications
from apps.catalog_medical_data.models import Disease, Medication


def create_diseases() -> None:
    """Функция для создания записей о болезнях."""
    for name, data in diseases.items():
        Disease.objects.get_or_create(
            name=name,
            defaults={'description': data['description']}
        )


def create_medications() -> None:
    """Функция для созднаия записей о лекарствах."""
    for name, data in medications.items():
        Medication.objects.get_or_create(
            name=name,
            defaults={
                'form': data['form'],
                'description': data['description']
            }
        )
