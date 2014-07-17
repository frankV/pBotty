from celery.schedules import crontab

BROKER_URL = 'sqla+mysql://root@localhost/celery_tasks'
CELERY_RESULT_BACKEND = "celery_tasks"
CELERY_RESULT_DBURI = 'mysql://root@localhost/celery_tasks'

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'tasks.add',
        'schedule': crontab(minute='*/1'),
        'args': (1,2),
    },
}