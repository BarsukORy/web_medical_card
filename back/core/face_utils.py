from insightface.app import FaceAnalysis
import numpy as np
from PIL import Image, ImageEnhance
import cv2
from pgvector.django import L2Distance

app = FaceAnalysis(name="buffalo_sc", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(256, 256))


def generate_face_vector_sync(photo):
    """Cинхронная функция для создания вектора лица."""
    try:
        img = Image.open(photo).convert('RGB')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        img_np = np.array(img)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        faces = app.get(img_cv)
        if not faces:
            raise ValueError('Лицо не обнаружено')
        face = faces[0]
        return face.embedding
    except Exception as e:
        raise ValueError(f'Ошибка при обработке изображения: {e}')


def get_similar_face_sync(vector, thresholed=25):
    """Синхронная функция для нахождения похожих лиц."""
    from apps.patient.models import Patient
    return Patient.objects.annotate(
        distance=L2Distance('face_vector', vector)
    ).filter(distance__lt=thresholed).order_by('distance')


def search_similar_faces_sync(photo, threshold=25):
    """Синхронная функция для поиска похожих пациентов."""
    try:
        vector = generate_face_vector_sync(photo)
        similar = get_similar_face_sync(vector, threshold)
        if not similar.exists():
            raise ValueError('Похожие пациенты не найдены')
        return similar
    except Exception as e:
        raise ValueError(e)
