# !/usr/bin/python3
# -*- coding: utf-8 -*-

from .base import *
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fastrunner_dev',  # 新建数据库
        # 'NAME': 'fast_mb4',  # 新建数据库名
        'HOST': '192.168.17.107',
        'USER': 'fastrunner',  # 数据库登录名
        'PASSWORD': 'fastrunner2020',  # 数据库登录密码
        'OPTIONS': {'charset': 'utf8mb4'},
        # 单元测试数据库
        'TEST': {
            'NAME': 'test_fast_last',  # 测试过程中会生成名字为test的数据库,测试结束后Django会自动删除该数据库
        }
    }
}
BROKER_URL = 'amqp://username:password@localhost:5672//'
