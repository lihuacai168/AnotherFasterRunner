# !/usr/bin/python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv, find_dotenv
from os import environ
from .base import *

DEBUG = False

# RabbitMQ和MySQL配置相关的设置
if find_dotenv():
    load_dotenv(find_dotenv())
    # RabbitMQ 账号密码
    MQ_USER = environ.get("RABBITMQ_DEFAULT_USER")
    MQ_PASSWORD = environ.get("RABBITMQ_DEFAULT_PASS")
    MQ_HOST = environ.get("MQ_HOST")

    SERVER_IP = environ.get("SERVER_IP")
    # 数据库账号密码
    MYSQL_HOST = environ.get("MYSQL_HOST")
    DB_NAME = environ.get("MYSQL_DATABASE")
    DB_USER = environ.get("MYSQL_USER")
    DB_PASSWORD = environ.get("MYSQL_PASSWORD")
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
        "ENGINE": "django.db.backends.mysql",
        "HOST": MYSQL_HOST,
        "NAME": DB_NAME,  # 新建数据库名
        "USER": DB_USER,  # 数据库登录名
        "PASSWORD": DB_PASSWORD,  # 数据库登录密码
        "OPTIONS": {"charset": "utf8mb4"},
        "TEST": {
            # 'MIRROR': 'default',  # 单元测试时,使用default的配置
            # 'DEPENDENCIES': ['default']
        },
    }
}

broker_url = f"amqp://{MQ_USER}:{MQ_PASSWORD}@{MQ_HOST}:5672//"

BASE_REPORT_URL = f"http://{SERVER_IP}:8000/api/fastrunner/reports"

# 用来直接url访问
# STATIC_URL = '/static/'

# 部署的时候执行python manage.py collectstatic，django会把所有App下的static文件都复制到STATIC_ROOT文件夹下
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 开发者模式中使用访问静态文
# STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "static"),
# )
