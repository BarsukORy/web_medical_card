from rest_framework import routers
from django.urls import path, include
from apps.patient import views

router = routers.DefaultRouter()
router.register(r'patients', views.PatientViewSet, basename='patient')

urlpatterns = [
    path('', include(router.urls)),
]