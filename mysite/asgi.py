### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

"""
ASGI config for mysite project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_asgi_application()
