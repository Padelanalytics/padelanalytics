"""
WSGI config for padelanalytics project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "padelanalytics.settings.prod")
# load secret variables. File is not to find at the repository!
SECRETS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "settings/secrets.py"
)
try:
    exec(open(SECRETS_FILE).read())
except Exception:
    pass
application = get_wsgi_application()
