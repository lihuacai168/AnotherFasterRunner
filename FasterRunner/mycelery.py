import logging
import os

from celery import Celery
from celery.signals import after_setup_logger, setup_logging

# set the default Django settings module for the 'celery' program.
from django.conf import settings

# from FasterRunner.settings import pro as settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FasterRunner.settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings.SETTINGS_MODULE)

app = Celery("FasterRunner")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings')
# app.config_from_object('FasterRunner.settings.pro')
obj = os.getenv("DJANGO_SETTINGS_MODULE")
app.config_from_object(obj, namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
    CELERY_BEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler",
    task_reject_on_worker_lost=True,
    task_acks_late=True,
    # celery worker的并发数 根据并发量是适当配置，不易太大
    CELERYD_CONCURRENCY=20,
    # 每个worker执行了多少次任务后就会死掉，建议数量大一些
    CELERYD_MAX_TASKS_PER_CHILD=300,
    # 每个worker一次性拿的任务数
    CELERYD_PREFETCH_MULTIPLIER=1,
    # 完全禁用 Celery 的日志配置
    worker_hijack_root_logger=False,
    worker_redirect_stdouts=False,
    worker_redirect_stdouts_level='ERROR',  # 只记录错误级别
)

# 禁用 Celery 的日志设置
@setup_logging.connect
def setup_loggers_without_celery(*args, **kwargs):
    return True
