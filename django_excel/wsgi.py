"""
WSGI config for django_excel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ['LC_ALL'] = 'en_NG.UTF-8'
os.environ['LANG'] = 'en_NG.UTF-8'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_excel.settings')

application = get_wsgi_application()
