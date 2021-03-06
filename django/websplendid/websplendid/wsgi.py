"""
WSGI config for websplendid project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import sys
sys.path.append('/home/bms/SplendidSnap/django/websplendid/')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websplendid.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
