"""
ASGI config for back project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import logging
import os
import django
from django.core.asgi import get_asgi_application

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Начало настройки ASGI")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
logger.debug("Установлена DJANGO_SETTINGS_MODULE")

django.setup()
logger.debug("Выполнен django.setup()")

application = get_asgi_application()
logger.debug("Создано ASGI application")

