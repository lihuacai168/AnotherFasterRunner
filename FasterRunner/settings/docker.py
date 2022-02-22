# !/usr/bin/python3
# -*- coding: utf-8 -*-

from .base import *
from os import environ

DEBUG = True
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
# IM_REPORT_SETTING.update({'platform_name': '银河飞梭测试平台'})
mq_user = environ.get('RABBITMQ_DEFAULT_USER')
mq_password = environ.get('RABBITMQ_DEFAULT_PASS')
BROKER_URL = f'amqp://{mq_user}:{mq_password}@mq:5672//'

# 需要先在RabbitMQ上创建fast_dev这个vhost
# BROKER_URL = 'amqp://admin:111111@192.168.22.19:5672/fast_dev'

BASE_REPORT_URL = 'http://localhost:8000/api/fastrunner/reports'

IM_REPORT_SETTING = {
    'base_url': 'http://localhost',
    'port': 8000,
    'report_title': '自动化测试报告'
}
