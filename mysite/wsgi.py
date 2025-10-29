### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

"""
WSGI config for mysite project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
