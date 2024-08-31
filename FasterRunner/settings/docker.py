# !/usr/bin/python3
# -*- coding: utf-8 -*-

from os import environ

from .base import *

DEBUG = False

# RabbitMQ和MySQL配置相关的设置

# RabbitMQ 账号密码
MQ_USER = environ.get("RABBITMQ_DEFAULT_USER")
MQ_PASSWORD = environ.get("RABBITMQ_DEFAULT_PASS")
MQ_PORT = environ.get("MQ_PORT")
MQ_HOST = environ.get("MQ_HOST", "mq")
MQ_VHOST = environ.get("MQ_VHOST", "/")


# 数据库账号密码
# FASTER_HOST = environ.get('FASTER_HOST')
DB_NAME = environ.get("MYSQL_DATABASE")
DB_PORT = environ.get("MYSQL_PORT", 3306)
DB_HOST = environ.get("MYSQL_HOST", "db")
DB_USER = environ.get("MYSQL_USER", "root")
DB_PASSWORD = environ.get("MYSQL_PASSWORD", "root")
PLATFORM_NAME = environ.get("PLATFORM_NAME")
if PLATFORM_NAME:
    IM_REPORT_SETTING.update({"platform_name": PLATFORM_NAME})

SENTRY_DSN = environ.get("SENTRY_DSN")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

DATABASES = {
    "default": {
        "ENGINE": "dj_db_conn_pool.backends.mysql",
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "NAME": DB_NAME,  # 新建数据库名
        "USER": DB_USER,  # 数据库登录名
        "PASSWORD": DB_PASSWORD,  # 数据库登录密码
        "OPTIONS": {"charset": "utf8mb4"},
        'POOL_OPTIONS': {
            'POOL_SIZE': 20,
            'MAX_OVERFLOW': 20,
            'RECYCLE': 24 * 60 * 60,
            'PRE_PING': True,
            'ECHO': False,
            'TIMEOUT': 30,
        },
    }
}

# mq_user = environ.get('FASTER_MQ_USER')
# mq_password = environ.get('FASTER_MQ_PASSWORD')
# broker_url = f'amqp://{mq_user}:{mq_password}@mq:5672//'
broker_url = f"amqp://{MQ_USER}:{MQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}/{MQ_VHOST}"

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SERVER_IP = environ.get("SERVER_IP", "")
DJANGO_API_PORT = environ.get("DJANGO_API_PORT", "8000")
BASE_REPORT_URL = f"http://{SERVER_IP}:{DJANGO_API_PORT}/api/fastrunner/reports"

IM_REPORT_SETTING = {
    "base_url": f"http://{SERVER_IP}",
    "port": environ.get("DJANGO_API_PORT", "8000"),
    "report_title": "自动化测试报告",
}
