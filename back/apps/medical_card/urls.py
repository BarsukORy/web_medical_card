from rest_framework import routers
from django.urls import path, include
from apps.medical_card import views

router = routers.DefaultRouter()

router.register(r'medical-cards',
                views.MedicalCardViewSet, basename='medical-card')
router.register(r'medical-cards/(?P<medical_card_id>\d+)/entries',
                views.MedicalCardEntryViewSet, basename='medical-card-entry')
router.register(r'medical-card-entries/(?P<medical_card_entry_id>\d+)/files',
                views.MedicalCardEntryFileViewSet, basename='medical-card-entry-file')
router.register(r'medical-card-entries/(?P<medical_card_entry_id>\d+)/prescriptions',
                views.PrescriptionViewSet, basename='prescription')
router.register(r'prescriptions/(?P<prescription_id>\d+)/medications',
                views.PrescriptionMedicationViewSet, basename='prescription-medication')

urlpatterns = [
    path('', include(router.urls)),
]