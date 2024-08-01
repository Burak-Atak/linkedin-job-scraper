from celery import Celery
import os

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkedin.settings')
app = Celery('linkedin')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
