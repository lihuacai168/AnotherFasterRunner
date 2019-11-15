from .base import *
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '10.0.3.57',
        'NAME': 'fast_last',  # 新建数据库名
        'USER': 'faster',  # 数据库登录名
        'PASSWORD': 'fast!~WB2019',  # 数据库登录密码
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            # 'MIRROR': 'default',  # 单元测试时,使用default的配置
            # 'DEPENDENCIES': ['default']
        }
    }
}