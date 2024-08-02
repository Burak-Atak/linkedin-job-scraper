from celery import Celery
import os

from django.conf import settings

from linkedin.celery_beat_scheduler import CELERYBEAT_SCHEDULE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linkedin.settings')
app = Celery('linkedin')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = CELERYBEAT_SCHEDULE
