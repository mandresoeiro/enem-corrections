"""
ASGI config for the ENEM Corrections backend.

This file exposes the ASGI callable as a module-level variable named ``application``.

It is used for:
- Async Django views
- WebSockets (future extension)
- ASGI servers like Uvicorn / Daphne
"""

import os
from django.core.asgi import get_asgi_application

# Load the correct environment settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

application = get_asgi_application()
