from rest_framework import routers
from django.urls import path, include
from apps.med_personal import views

router = routers.DefaultRouter()

router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'registrar', views.RegistrarViewSet, basename='registrar')

urlpatterns = [
    path('', include(router.urls)),
]