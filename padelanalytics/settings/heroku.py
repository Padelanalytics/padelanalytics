import django_heroku

from .dev import *  # noqa: F403, F401

INSTALLED_APPS += (  # noqa: F405
    'django_heroku',
)

# Configure Django App for Heroku.
django_heroku.settings(
    locals(),
    databases=False,
)
