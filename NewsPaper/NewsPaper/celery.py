from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsProject.settings')

app = Celery('NewsProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_news_email': {
        'task': 'news.tasks.send_weekly_news_email',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}