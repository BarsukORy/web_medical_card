from rest_framework import routers
from apps.custom_user import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'auth', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]