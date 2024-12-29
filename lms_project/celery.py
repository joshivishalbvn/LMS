from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')

app = Celery('lms_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#register class based view 
from app_modules.users.tasks import SendUserCredentialsEmail
app.register_task(SendUserCredentialsEmail())

# to start celery worker for this project
# celery -A lms_project worker --loglevel=info

# to monitor celery use this command
# celery -A lms_project flower
