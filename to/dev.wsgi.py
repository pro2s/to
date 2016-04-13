"""
WSGI config for it project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append('/var/www/django/devto')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "to.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
