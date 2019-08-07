import os
from celery import Celery
from celery.schedules import crontab
# from app.main import GirosApp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuexperto.settings')

app = Celery('tuexperto')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

