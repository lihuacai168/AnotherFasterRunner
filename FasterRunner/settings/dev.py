# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from .base import *

DEBUG = True

# LOGGING["loggers"]["mock"]["level"] = "DEBUG"

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS}"
    " [pid:{process} -> thread:{thread.name}]"
    " {level}"
    " [{name}:{function}:{line}]"
    " {message}",
    level="DEBUG",
)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "fast",  # 新建数据库
        # 'NAME': 'fast_mb4',  # 新建数据库名
        "HOST": "127.0.0.1",
        "USER": "root",  # 数据库登录名
        "PASSWORD": "root",  # 数据库登录密码
        "OPTIONS": {"charset": "utf8mb4"},
        # 单元测试数据库
        "TEST": {
            "NAME": "test_fast_last",  # 测试过程中会生成名字为test的数据库,测试结束后Django会自动删除该数据库
        },
    }
}
# IM_REPORT_SETTING.update({'platform_name': '银河飞梭测试平台'})

BROKER_URL = "amqp://username:password@localhost:5672//"
# 需要先在RabbitMQ上创建fast_dev这个vhost

broker_url = "amqp://admin:111111@192.168.22.19:5672/fast_dev"


BASE_REPORT_URL = "http://localhost:8000/api/fastrunner/reports"

IM_REPORT_SETTING = {
    "base_url": "http://localhost",
    "port": 8000,
    "report_title": "自动化测试报告",
}
