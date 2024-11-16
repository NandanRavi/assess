from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assessmentProject.settings')

app = Celery('assessmentProject')

app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'send-mail-every-day-at-8':  {
        'task': 'users.tasks.send_mail_func',
        'schedule': crontab(hour=15, minute=42, day_of_month=25, month_of_year=10),

    }

}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request:{self.request!r}")
