from .base import *
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fast',  # 新建数据库名
        'USER': 'root',  # 数据库登录名
        'PASSWORD': 'root',  # 数据库登录密码
        # 单元测试数据库
        'TEST': {
            'NAME': 'test_fast_last',  # 测试过程中会生成名字为test的数据库,测试结束后Django会自动删除该数据库
        }
    }
}