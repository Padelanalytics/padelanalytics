"""
WSGI config for padelanalytics project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
from wsgi_basic_auth import BasicAuth

application = BasicAuth(get_wsgi_application())
