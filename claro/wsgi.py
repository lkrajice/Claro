"""
WSGI config for claro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os
import logging

from claro.utils import Scheduler
from votes.models import schedule_db_updates

from django.core.wsgi import get_wsgi_application

# setup logger
formatter = logging.Formatter('[%(asctime)s | %(levelname)-10s | %(module)-10s]: %(message)s')

file_handler = logging.FileHandler('claro.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

LOG = logging.getLogger()
LOG.addHandler(file_handler)
LOG.addHandler(stream_handler)
LOG.setLevel(logging.DEBUG)

scheduler = Scheduler()
scheduler.run()

schedule_db_updates()

# Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "claro.settings")

application = get_wsgi_application()
