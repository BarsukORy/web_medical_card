from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.medical_hub import views

router = DefaultRouter()

router.register(r'hospitals', views.HospitalViewSet, basename='hospital')
router.register(r'specialities', views.SpecialtyViewSet, basename='specialty')

urlpatterns = [
    path('', include(router.urls)),
]