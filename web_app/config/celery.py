from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.broker_url = 'redis://redis_q:6379/0'
app.conf.result_backend = 'redis://redis_q:6379/1'

app.autodiscover_tasks()

app.conf.task_create_missing_queues = True
app.conf.worker_prefetch_multiplier = 1

app.conf.update(worker_max_tasks_per_child=10)
