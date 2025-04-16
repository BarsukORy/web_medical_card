from rest_framework import routers
from apps.catalog_medical_data import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'diseases', views.DiseaseViewSet, basename='disease')
router.register(r'medications', views.MedicationViewSet, basename='medication')

urlpatterns = [
    path('', include(router.urls)),
]