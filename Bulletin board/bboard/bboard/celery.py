import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bboard.settings')

app = Celery('bboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_mail_8am': {
        'task': 'project.tasks.weekly_mailing_list',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),

    }
}