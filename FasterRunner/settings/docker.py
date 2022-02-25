# !/usr/bin/python3
# -*- coding: utf-8 -*-

from .base import *
from os import environ

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fast_db',  # 新建数据库
        # 'NAME': 'fast_mb4',  # 新建数据库名
        'HOST': 'db',
        'USER': 'root',  # 数据库登录名
        'PASSWORD': 'root',  # 数据库登录密码
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

mq_user = environ.get('RABBITMQ_DEFAULT_USER')
mq_password = environ.get('RABBITMQ_DEFAULT_PASS')
BROKER_URL = f'amqp://{mq_user}:{mq_password}@mq:5672//'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

BASE_REPORT_URL = 'http://localhost:8000/api/fastrunner/reports'

IM_REPORT_SETTING = {
    'base_url': 'http://localhost',
    'port': 8000,
    'report_title': '自动化测试报告'
}
