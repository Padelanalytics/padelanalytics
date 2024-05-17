import django_heroku

from .dev import *  # noqa: F403, F401

INSTALLED_APPS += ("django_heroku",)  # noqa: F405

# Configure Django App for Heroku.
django_heroku.settings(
    locals(),
    databases=False,
)
