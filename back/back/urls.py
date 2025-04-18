from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('apps.catalog_medical_data.urls')),
    path('auth/', include('apps.custom_user.urls')),
    path('med_personal/', include('apps.med_personal.urls')),
    path('medical_card/', include('apps.medical_card.urls')),
    path('medical_hub/', include('apps.medical_hub.urls')),
    path('patient/', include('apps.patient.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)