"""
WSGI config for the ENEM Corrections backend.

Exposes the WSGI callable as a module-level variable named ``application``.
Used for production servers like Gunicorn.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

application = get_wsgi_application()
