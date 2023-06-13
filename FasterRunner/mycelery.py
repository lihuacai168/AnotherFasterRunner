import logging
import os
from celery import Celery
from celery.signals import after_setup_logger

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
    CELERYD_CONCURRENCY=1 if settings.DEBUG else 4,
    # 每个worker执行了多少次任务后就会死掉，建议数量大一些
    CELERYD_MAX_TASKS_PER_CHILD=100,
    # 每个worker一次性拿的任务数
    CELERYD_PREFETCH_MULTIPLIER=1,
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_FORCE_EXECV=True,  # 有些情况可以防止死锁
    CELERY_TASK_TIME_LIMIT=3*60*60,  # 单个任务最大运行时间
)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    fh = logging.FileHandler("logs/celery.log", "a", encoding="utf-8")
    fh.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s  %(levelname)s  [pid:%(process)d] [%(name)s %(filename)s->%(funcName)s:%(lineno)s] %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
