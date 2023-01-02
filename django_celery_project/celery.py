from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_project.settings')

app = Celery('django_celery_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Seoul')

app.config_from_object(settings, namespace='CELERY')


# Celery Beat Setting
# celery -A django_celery_project beat -l info
# beat가 실행될때, 실제 메일이 보내지려면, celery worker도 별도로 실행시켜놔야 한다. 
# 즉, $ celery -A django_celery_project worker -l info
app.conf.beat_schedule = {
    'send-mail-every-day-at-8' : {
        'task': 'send_mail_app.tasks.send_mail_func',
        'schedule': crontab(hour=1, minute=50, day_of_month=3, month_of_year=1),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')