# -*- coding: utf-8 -*-

from ..extensions import celery, db
from flask.globals import current_app
from celery.signals import task_postrun


celery = Celery('tasks')
celery.config_from_object('celeryconfig')

@celery.task
def do_some_stuff():
    current_app.logger.info("I have the application context")
    #you can now use the db object from extensions

    return x + y
    from celery import Celery


@celery.task
def add(x, y):
    return x + y

@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()